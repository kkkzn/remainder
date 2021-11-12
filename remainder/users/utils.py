"""
With Flask-mail, didn't succeed in sending a reset email from G-mail account.
So decided to use smtplib and email packages instead.
"""
import os
from dotenv import load_dotenv

from flask import url_for
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate, formataddr
from email.header import Header


def config_reset_email(user):
    load_dotenv()

    # get token
    token = user.get_reset_token()

    # compose a message
    config = {
        'subject': 'Password Reset',
        'bodyText': f"""Hi {user.username},\n\nSomeone recently requested a password change for your REMAINDER account. 
If this was you, you can set a new password here:\n{url_for('users.reset_token', token=token, _external=True)}\n
If you don't want to change your password or didn't request this, just ignore and delete this message.\n
To keep your account secure, please don't forward this email to anyone.\n
Cheers,\n
Remainder Admin\nREMAINDER\nhttps://remainder-app.herokuapp.com/""",
        'fromAddress': os.environ.get('EMAIL_REMAINDER'),
        'toAddress': user.email
    }

    return config


def send_email(config):
    load_dotenv()

    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    # connect to smtp server and login
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    smtpobj.login(MAIL_USERNAME, MAIL_PASSWORD)

    # compose an email
    msg = MIMEText(config['bodyText'])
    msg['Subject'] = config['subject']
    msg['From'] = formataddr((str(Header('REMAINDER Admin', 'utf-8')), config['fromAddress']))
    msg['To'] = config['toAddress']
    msg['Date'] = formatdate()

    # send the email out
    smtpobj.send_message(msg)
    smtpobj.close()
