'''
app.py is the main entry point for the Flask application.
It contains the routes and logic for the web application, including rendering templates,
handling form submissions, and interacting with the database.
'''

from flask import Flask, render_template, jsonify, request, url_for, redirect
from logger_db import DatabaseThread
import webbrowser
import os
from sample_logs_generator import LogGenerator
from threading import Thread
from dev_interactions import FW_LOG_MODULE_TYPE
from forms import LogGenForm, FilterForm
from log_reader import LogReader
from log_def import Log

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

db_thread = DatabaseThread('logs.db')
gen = LogGenerator(db_thread)

@app.route('/', methods=['GET'])
def index():
    """
    Renders the static_page.html template.

    Returns:
        The rendered static_page.html template.
    """
    return render_template('landing_page.html')

@app.route('/get_logs', methods=['GET'])
def get_logs():
    """
    Retrieve all logs from the database and render them in the log_viewer.html template.

    Returns:
        The rendered template with the logs.
    """
    logs = db_thread.get_all_logs()
    print(logs[-1])
    filter_form = FilterForm()
    return render_template('log_viewer.html', logs=logs, log_groups=FW_LOG_MODULE_TYPE, filter_form=filter_form)

@app.route('/latest_logs', methods=['GET'])
def get_latest_logs():
    """
    Retrieve the latest logs from the database.

    Returns:
        The latest logs in JSON format.
    """
    try:
        logs = db_thread.get_new_logs()
        return jsonify(data=[log.to_dict() for log in logs]), 200
    except Exception as e:
        print(e)
        return str(e), 500

@app.route('/generator_page', methods=['GET', 'POST'])
def generator_page():
    """
    Renders the log generator page template.

    Returns:
        The rendered log generator page template.
    """
    log_generator_form = LogGenForm()
    if request.method == 'POST':
        if log_generator_form.validate_on_submit():
            num_of_logs = log_generator_form.num_of_logs.data
            delay_betweeen_logs = log_generator_form.delay_betweeen_logs.data
            # Start a new thread that runs the slow_log_gen function
            thread = Thread(target=gen.slow_log_gen, args=(num_of_logs, delay_betweeen_logs))
            thread.start()
            return redirect(url_for('index'))

    return render_template('log_generator.html', log_generator_form=log_generator_form)

@app.route('/upload_logs', methods=['POST'])
def upload_logs():
    data = request.get_json()
    file_path = data['filePath']

    if not os.path.exists(file_path):
        print(f'File does not exist at {file_path}')
        return jsonify({'error': 'File does not exist'}), 400

    # Process the file at file_path
    # ...

    return (jsonify({'message': 'File processed successfully'}), 200)

@app.route('/clear_logs', methods=['GET'])
def clear_logs():
    """
    Clear all logs from the database.

    Returns:
        A JSON response with a message indicating that the logs were cleared.
    """
    db_thread.clear_logs()
    return jsonify(message='Logs cleared')

@app.route('/start_device', methods=['GET'])
def start_device():
    """
    Start a process, that will start a device that generates logs.
    Also another process will read the logs and insert them into the database.

    Returns:
        A JSON response with a message indicating that the device was started.
    """
    # Start a thread that will run the LogReader class
    log_reader = LogReader()

    return jsonify(message='Device started')

def get_app():
    return app

@app.route('/filter_logs', methods=['GET', 'POST'])
def filter_logs():
    """
    Filter logs based on user input.

    This function handles the filtering of logs based on the user's input from the filter form.
    It retrieves the column name and filter value from the form, and uses them to filter the logs
    using the `filter_logs` method of the `db_thread` object. The filtered logs are then passed to
    the log_viewer.html template along with the log groups and filter form.

    Returns:
        The rendered log_viewer.html template with the filtered logs, log groups, and filter form.
    """
    filter_form = FilterForm()
    if request.method == 'POST':
        if filter_form.validate_on_submit():
            column_name = filter_form.column_name.data
            filter_value = filter_form.filter_value.data
            logs = db_thread.filter_logs(column_name, filter_value)
            for log in logs:
                print(log.timestamp)
                print(log.file)
                print(log.src_function_name)
                print(log.level)
                print(log.log_group.name)
                print(log.msg)
            return render_template('log_viewer.html', logs=logs, log_groups=FW_LOG_MODULE_TYPE, filter_form=filter_form)
    return render_template('log_viewer.html', flogs=logs, log_groups=FW_LOG_MODULE_TYPE, filter_form=filter_form)

if __name__ == '__main__':
    url = "http://localhost:8080/"
    webbrowser.open(url, new=2)  # open in new tab, if possible
    app.run(debug=True, port=8080)
    db_thread.close()
    os.remove('logs.db')
