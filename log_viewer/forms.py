from wtforms import validators, IntegerField, SubmitField, StringField, SelectField
from flask_wtf import FlaskForm
from log_def import Log


class LogGenForm(FlaskForm):
    """
    A form for generating logs.
    """
    num_of_logs = IntegerField('Number of Logs', [validators.InputRequired(
    ), validators.NumberRange(min=1, max=100000)], default=1000)
    delay_betweeen_logs = IntegerField('Delay Between Logs (ms)', [
                                       validators.InputRequired(), validators.NumberRange(min=500, max=5000)], default=500)
    submit = SubmitField('Generate Logs')


class FilterForm(FlaskForm):
    """
    Represents a form used for filtering logs.

    Attributes:
        column_name (SelectField): The select field for choosing the column name.
        filter_value (StringField): The text field for entering the filter value.
        submit (SubmitField): The submit button for applying the filter.
    """
    column_name = SelectField('Column Name')
    filter_value = StringField('Filter Value', [validators.InputRequired()])
    submit = SubmitField('Filter')

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.column_name.choices = [(column, column) for column in Log.__table__.columns.keys()]

class StartDeviceForm(FlaskForm):
    """
    Represents a form used for starting a device.

    Attributes:
        device_id (StringField): The text field for entering the device ID.
        submit (SubmitField): The submit button for starting the device.
    """
    device_id = StringField('Device ID', [validators.InputRequired()])
    submit = SubmitField('Start Device')