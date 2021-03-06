import pytz

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from remainder.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=2, max=20), DataRequired()])
    email = StringField('Email',
                        validators=[Email(), DataRequired()])
    timezone_region = SelectField('Timezone(Region)', validators=[DataRequired()],
                                  choices=[
                                  'Africa', 'America', 'America/Argentina',
                                  'America/Indiana', 'America/Kentucky', 'America/North_Dakota',
                                  'Antarctica', 'Arctic', 'Asia', 'Atlantic', 'Australia',
                                  'Canada', 'Europe', 'Indian', 'Pacific','US'
                                  ])
    timezone_city = SelectField('Timezone(City)', validators=[DataRequired()],
                                choices=[])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Sign Up')

    # check if the new user chooses a unique name
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    timezone = SelectField('Timezone (Region/City)', validators=[DataRequired()],
                           choices=pytz.common_timezones)
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
