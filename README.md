# REMAINDER
REMAINDER is a time recording web application with functionality such as:

- record keeping for wake-up time and bed time
- visualization of the remaining time of the day
- visualization of your wake-up time, bed-time, and sleep hours over a period of time (max: 14 days)

## Video Demo:  <URL HERE>

## Description: 
  REMAINDER estimates the remaining time of the day from your wake-up time and average hours of sleep with the following logic:
  (the order of calculation is 3 => 2 => 1)  
  1. [remaining time] = *[estimated bed-time of the day]* - [current time]   
  2. *[estimated bed-time of the day]* = [wake-up time] + *[average hours of being awake]*    
  3. *[average hours of being awake]* = 24hrs - [average hours of sleep]  
  
  Other important features are:
  - App supports common timezones.
  - App visualizes the remainder of the day as a pie chart.
  - App visualizes your sleep habit (wake-up, bed, sleep hours) in bar charts.
  - User can download your wake-up time and bed time in a csv file.
  - User can upload sleep data (wake-up time and bed time) through csv file.
  - User can retrieve password through Forgot Password? link. (A secure password reset token will be sent to user's email.)
  
## Note:  
  REMAINDER is currently hosted by heroku with "free" plan, so will idle (sleep) after a period of inactivity.  
  The next request will wake it up, but users will notice a delay while the app is started.
    
## Built with: 
  FLASK   
  Bootstrap  
  JQuery  
  Heroku  

## Usage:
  Visit: https://remainder-app.herokuapp.com/ , create an account with your email, then start adding records.

## Design choices:
  - Ranges of sleep-habit bar charts are arbitrarily set. I hope this design prompts users to manage their sleep-habit not to go beyond these ranges:
    - 4 hours to 10 hours for sleep hour
    - 5 am to 11 am for wake-up time
    - 9 pm to 3 am for bed time  
  
  - The options of Timezone field on Account page are too broad. I tried my best to separate the field into Region and City and make them dynamic in the same way as the field on Registration page does: selecting Region narrows down the list of City options, but couldn't make it. I'm hoping that users don't relocate across timezones so often.
  
## Contact:
  - kkkzn - email - kznrod@gmail.com 
  - Project link: https://github.com/kkkzn/remainder
