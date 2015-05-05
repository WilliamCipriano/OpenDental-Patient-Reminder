# OpenDental-Patient-Reminder
Daily reminder for your patients from opendental.

Patient activator cost = $200 month  
Callfire text message cost = $0.05  
Twilio text message cost  = $0.0075  

Simple install instructions (for windows):  
These instructions are for installs on the server but there is no reason why you can't run it someplace else. This is assuming you have a fairly standard OpenDental setup but should work for most of them. This is only a mildly technical install but I recommend backing up your database before attempting any of this (in fact I run  [this](https://github.com/WilliamCipriano/WillBackup "WillBackup") hourly to prevent and issues. Please send any bugs or issues to ODPR@wfc.help.

1. Install python 2.7.9 [Here](https://www.python.org/downloads/ "Python 2.7 install")
2. Install MySql's python connector [Here](https://dev.mysql.com/downloads/connector/python/ "MySql python connector")
3. Install twilio's python module [Here](https://www.twilio.com/docs/python/install "twilio python module")
4. Modify config.ini to match your twillio settings.
5. Modify OD-Appointment-Sender.py to reflect your database details.
6. Set up a task with windows task scheduler to be run daily.


config.ini Example:  
SID = Your SID  
AUTH = Your auth key  
NUMBER = The phone number  
