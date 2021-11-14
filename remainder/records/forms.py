from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import InputRequired


class SleepRecordForm(FlaskForm):
    up = DateTimeLocalField('Up', default=datetime.today,
                            format='%Y-%m-%dT%H:%M',
                            validators=[InputRequired()])
    to_bed = DateTimeLocalField('To-bed', default=datetime.today,
                                format='%Y-%m-%dT%H:%M',
                                validators=[InputRequired()])
    submit = SubmitField('Save')


class UploadForm(FlaskForm):
    csv = FileField('CSV', validators=[FileRequired(), FileAllowed(['csv'])])
    submit = SubmitField('Upload')

    """
    Validation to make sure that csv has the valid format.
    Don't know why, but if include this validation, uploaded csv.data will become empty. 

    def validate_csv(self, csv):
        csv_data = pd.read_csv(csv.data)
        # check the first row of csv
        VALID_COL_STRFORM = ["Index(['up', 'to_bed'], dtype='object')",
                             "Index(['to_bed', 'up'], dtype='object')"]
        if not str(csv_data.columns) in VALID_COL_STRFORM:
            raise ValidationError('The first row of csv must be two field long: ["up", "to_bed"] or ["to_bed", "up"]')
    """
