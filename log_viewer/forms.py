from wtforms import Form, validators, IntegerField, SubmitField
from flask_wtf import FlaskForm

class LogGenForm(FlaskForm):
    """
    A form for generating logs.
    """
    num_of_logs = IntegerField('Number of Logs', [validators.InputRequired(), validators.NumberRange(min=1, max=100000)], default=1000)
    delay_betweeen_logs = IntegerField('Delay Between Logs (ms)', [validators.InputRequired(), validators.NumberRange(min=1, max=1000)], default=100)
    submit = SubmitField('Generate Logs')
