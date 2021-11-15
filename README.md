# REMAINDER
REMAINDER is a time recording web application with functionality such as:

- record keeping for wake-up time and bed time
- visualization of the remaining time of the day
- visualization of the variations of wake-up time, bed-time, and sleep hours over a period of time (max: 14 days)

## Video Demo:  <URL HERE>

## Description: 

REMAINDER
- estimate the remaining time of the day from your wake-up time and average hours of sleep.  
  Formula is as follows:  
  [remaining time] = *[estimated bed-time of the day]* - [current time]  
  *[estimated bed-time of the day]* = [wake-up time] + *[average hours of being awake]*  
  *[average hours of being awake]* = 24hrs - [average hours of sleep]  
- visualize the remainder of the day as a pie chart.
- visualize the varitations of your sleep habit (wake-up, bed, sleep hours) in bar charts.
- let you download your wake-up time and bed time in a csv file.
- import your data (wake-up time and bed time) through csv file, if you keep records of them in csv.
This web application is hosted by heroku with "free" plan, so will idle (sleep) after a period of inactivity. The next request will wake it up, but users will notice a delay while the app is started.


## Requirement: 

alembic==1.7.4
bcrypt==3.2.0
blinker==1.4
cffi==1.15.0
click==8.0.3
cycler==0.10.0
decorator==5.1.0
dnspython==2.1.0
email-validator==1.1.3
Flask==2.0.2
Flask-Bcrypt==0.7.1
Flask-Login==0.5.0
Flask-Migrate==3.1.0
flask-paginate==2021.10.29
Flask-SQLAlchemy==2.5.1
Flask-WTF==0.15.1
greenlet==1.1.2
gunicorn==20.1.0
idna==3.3
infinity==1.5
intervals==0.9.2
itsdangerous==2.0.1
Jinja2==3.0.2
kiwisolver==1.3.2
Mako==1.1.5
MarkupSafe==2.0.1
matplotlib==3.4.3
numpy==1.21.3
pandas==1.3.4
Pillow==8.4.0
psycopg2==2.9.2
pycparser==2.20
pyparsing==3.0.3
python-dateutil==2.8.2
python-dotenv==0.19.1
pytz==2021.3
scipy==1.7.1
seaborn==0.11.2
six==1.16.0
SQLAlchemy==1.4.26
validators==0.18.2
Werkzeug==2.0.2
WTForms==2.3.3
WTForms-Components==0.10.5

## Usage:

Visit: https://remainder-app.herokuapp.com/ 
Create an account with your email, and add records.

## Note:



## Contact:

- kkkzn - email - kznrod@gmail.com 
- Project link: 
