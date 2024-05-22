from wtforms import validators, IntegerField, SubmitField
from flask_wtf import FlaskForm

class LogGenForm(FlaskForm):
    """
    A form for generating logs.
    """
    num_of_logs = IntegerField('Number of Logs', [validators.InputRequired(), validators.NumberRange(min=1, max=100000)], default=1000)
    delay_betweeen_logs = IntegerField('Delay Between Logs (ms)', [validators.InputRequired(), validators.NumberRange(min=500, max=5000)], default=500)
    submit = SubmitField('Generate Logs')
