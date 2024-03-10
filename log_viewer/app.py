from flask import Flask, render_template
from logger_db import DatabaseThread
from logger_db import Log

app = Flask(__name__)

db_thread = DatabaseThread('logs.db')
db_thread.start()


@app.route('/', methods=['GET'])
def index():
    return render_template('static_page.html')


@app.route('/logs', methods=['GET'])
def get_logs():
    logs = db_thread.get_all_logs()
    return render_template('log_viewer.html', logs=logs)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
    db_thread.close()
