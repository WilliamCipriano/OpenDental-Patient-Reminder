# OpenDental-Patient-Reminder
Daily reminders and automatic patient confirmation for your clients from within opendental.

Patient activator cost = $200 / month  
Callfire cost = $0.05 / text  
Twilio cost  = $0.0075 / text

Simple install instructions (for windows):  
These instructions are for installs on the server but there is no reason why you can't run it someplace else. This is assuming you have a fairly standard OpenDental setup but should work for most of them. This is only a mildly technical install (some knowledge of python might come in handy, but is not required) but I recommend backing up your database before attempting any of this (in fact I run  [this](https://github.com/WilliamCipriano/WillBackup "WillBackup") hourly to prevent any problems.) Please send any bugs or issues to ODPR@wfc.help.

1. Install python 2.7.9 [Here](https://www.python.org/downloads/ "Python 2.7 install")
2. Install MySql's python connector [Here](https://dev.mysql.com/downloads/connector/python/ "MySql python connector")
3. Install twilio's python module [Here](https://www.twilio.com/docs/python/install "twilio python module")
4. Install flask [Here](http://flask.pocoo.org/ "Flask")
5. Download and copy OpenDental-Patient-Reminder to your hard drive.
6. Modify config.ini to match your twillio settings.
7. Modify OD-Appointment-Sender.py and listen.py to reflect your database details.
8. Set up a task with windows task scheduler to be run daily.
9. Forward port 5000 to the server this is going to be run on.
10. Run listen.py to automaticaly confirm appointments.


config.ini Example:  
SID = Your SID  
AUTH = Your auth key  
NUMBER = The phone number  

OD-Appointment-Sender.py Example:  
config = {  
  'user': 'root',  
  'password': '',  
  'host': '127.0.0.1',  
  'database': 'opendental',  
  'raise_on_warnings': True,  
}

Version Log:  
ALPHA  
0.0.1 - Added basic reminder functionalty  
0.0.2 - Added abilty to automatically confirm patients  
0.0.3 - Added email status alerts  
0.0.4 - Begin creating reporting functionalty and dormant patient reactivation
