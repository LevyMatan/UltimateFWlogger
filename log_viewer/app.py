from flask import Flask, render_template, jsonify, request
from logger_db import DatabaseThread, Log
import webbrowser
import os
from sample_logs_generator import LogGenerator
app = Flask(__name__)

db_thread = DatabaseThread('logs.db')
gen = LogGenerator(db_thread, 100)
gen.write_logs_to_db()

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

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Retrieve all logs from the database and render them in the log_viewer.html template.

    Returns:
        The rendered template with the logs.
    """
    logs = db_thread.get_all_logs()
    # set an array of 5 colors for highlighting:
    colors = [# light blue
              '#ADD8E6',
              # light green
              '#90EE90',
              # light yellow
              '#FFFFE0',
              # light pink
              '#FFB6C1',
              # light orange
              '#FFD700']
    return render_template('log_viewer.html', logs=logs, colors=colors)

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

@app.route('/generator', methods=['GET'])
def generator_page():
    """
    Renders the log generator page template.

    Returns:
        The rendered log generator page template.
    """
    return render_template('log_generator.html')

@app.route('/sample_log_gen', methods=['GET'])
def sample_log_gen():
    """
    Generate sample logs and write them to the database.

    Returns:
        The rendered log generator page template.
    """
    num_of_logs = request.args.get('num_of_logs', type=int)
    max_delay_ms = request.args.get('max_delay_ms', type=int)
    gen.slow_log_gen(num_of_logs=num_of_logs, max_delay=max_delay_ms)


if __name__ == '__main__':
    url = "http://localhost:8080/"
    webbrowser.open(url, new=2)  # open in new tab, if possible
    app.run(debug=True, port=8080)
    db_thread.close()
    # Delete the DB file
    os.remove('logs.db')
