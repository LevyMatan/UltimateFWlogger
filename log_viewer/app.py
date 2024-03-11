from flask import Flask, render_template
from logger_db import DatabaseThread
import webbrowser

app = Flask(__name__)

db_thread = DatabaseThread('logs.db')
db_thread.start()


@app.route('/', methods=['GET'])
def index():
    return render_template('static_page.html')


@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Retrieve all logs from the database and render them in the log_viewer.html template.

    Returns:
        The rendered template with the logs.
    """
    logs = db_thread.get_all_logs()
    return render_template('log_viewer.html', logs=logs)


if __name__ == '__main__':
    url = "http://localhost:8080/"
    webbrowser.open(url, new=2)  # open in new tab, if possible
    app.run(debug=True, port=8080)
    db_thread.close()
