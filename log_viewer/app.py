from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/logs', methods=['GET'])
def get_logs():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()

    c.execute("SELECT * FROM logs")
    logs = c.fetchall()

    return render_template('log_viewer.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)