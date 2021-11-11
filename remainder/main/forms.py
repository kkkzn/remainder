from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    firstname = StringField(label='First Name', validators=[DataRequired()])
    lastname = StringField(label='Last Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    message = TextAreaField(label='Message', validators=[DataRequired()])
    submit = SubmitField(label="Submit")
