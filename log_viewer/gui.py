'''
This is the GUI module for the log viewer application. It contains the main window and the log viewer widget.
'''

from flaskwebgui import FlaskUI
from app import get_app


if __name__ == '__main__':
    # Create the Flask app
    app = get_app()
    FlaskUI(app=app, server="flask", width=600, height=500).run()
