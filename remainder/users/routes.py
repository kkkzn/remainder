from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from remainder import db, bcrypt
from remainder.models import User, Timezone
from remainder.users.forms import (RegistrationForm, LoginForm, RequestResetForm,
                                   ResetPasswordForm, UpdateAccountForm)
from remainder.users.utils import config_reset_email, send_email


users_bp = Blueprint('users', __name__)


@users_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    form.timezone_city.choices = [(tz.id, tz.city) for tz in Timezone.query.all()]
    if form.validate_on_submit():
        tz = Timezone.query.filter_by(id=form.timezone_city.data).first()
        region = form.timezone_region.data
        timezone = f'{region}/{tz.city}'
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    timezone=timezone, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@users_bp.route("/timezone/<region>")
def timezone(region):
    timezones = Timezone.query.filter_by(region=region).all()
    tz_list = []
    for tz in timezones:
        tzObj = {'id': tz.id, 'city': tz.city}
        tz_list.append(tzObj)

    return jsonify({'timezones': tz_list})


@users_bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@users_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.timezone = form.timezone.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.timezone.data = current_user.timezone
    return render_template('users/account.html', title='Account',
                           form=form)


@users_bp.route("/user/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(config_reset_email(user))
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Reset Password',
                           form=form)


@users_bp.route("/user/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in with the new password.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', title='Reset Password',
                           form=form)
