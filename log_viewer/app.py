from flask import Flask, render_template, jsonify, request, url_for, redirect
from logger_db import DatabaseThread, Log
import webbrowser
import os
from sample_logs_generator import LogGenerator
from threading import Thread
from dev_interactions import FW_LOG_MODULE_TYPE
from flaskwebgui import FlaskUI
from forms import LogGenForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
ui = FlaskUI(app, port=8080)

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

@app.route('/logs/filter/<attribute>/<value>', methods=['GET'])
def set_log_filter(attribute, value, operator='=='):
    """
    Set the filter for the logs.

    Args:
        attribute (str): The attribute to filter on: 'level', 'file', 'src_function_name'.
        value (str): The value to filter on.
        operator (str): The operator to use for the filter (e.g., '==', '!=').

    Returns:
        None
    """
    db_thread.set_logs_filter(attribute, value, operator)
    print(f'Filter set: {attribute} {operator} {value}')
    return get_logs()

@app.route('/get_logs', methods=['GET'])
def get_logs():
    """
    Retrieve all logs from the database and render them in the log_viewer.html template.

    Returns:
        The rendered template with the logs.
    """
    logs = db_thread.get_all_logs()
    return render_template('log_viewer.html', logs=logs, log_groups=FW_LOG_MODULE_TYPE)

@app.route('/unique/<column>')
def get_unique_values(column):
    """
    Retrieve unique values from a specific column in the database.

    Args:
        column (str): The name of the column to retrieve unique values from.

    Returns:
        list: A list of unique values from the specified column.
    """
    unique_values = db_thread.session.query(getattr(Log, column)).distinct().all()
    return jsonify([value[0] for value in unique_values])

@app.route('/latest_logs', methods=['GET'])
def get_latest_logs():
    """
    Retrieve the latest logs from the database.

    Returns:
        The latest logs in JSON format.
    """
    logs = db_thread.get_new_logs()
    return jsonify(data=[log.to_dict() for log in logs])

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

@app.route('/log_group', methods=['POST'])
def log_group():
    """
    Set the log group for the logs.

    Returns:
        A JSON response with a message indicating that the log group was set.
    """
    data = request.get_json()
    log_group = data['log_group']
    db_thread.set_logs_filter('log_group', log_group)
    return jsonify(message='Log group set')

if __name__ == '__main__':
    url = "http://localhost:8080/"
    webbrowser.open(url, new=2)  # open in new tab, if possible
    app.run(debug=True, port=8080)
    # ui.run()
    db_thread.close()
    # Delete the DB file
    os.remove('logs.db')
