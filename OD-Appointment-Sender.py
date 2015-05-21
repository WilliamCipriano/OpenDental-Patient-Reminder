import mysql.connector
from datetime import datetime, timedelta
import time
import text
import time
import log

#Written by: Will Cipriano, willcipriano.com

#this accesses the OpenDental database and then loads all the patients with appointments for today, then uses text.msg() to send them to the respective phone numbers.
#This depends on the twillo python module as well as mysql.connector.

#Office Details
address = "123 fake street"
callbacknumber = "(555)-1212"
email_logs = True

#Variables
delta24h = timedelta(hours=13)
date = time.strftime("%Y-%m-%d")
patient_cell_number = []
patient_appointment_time = []

#Will not send reminders to patients scheduled before this time.
reminder_hour = 9
#How many seconds to wait before closing the program.
wait_on_close = 30
#How many seconds to wait between messages.
send_delay = 1

#Define database location and information here, if you are paranoid you can compile this to a .pyc to prevent a casual attacker.
config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'database': 'opendental',
  'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

log.write("\n Beginning to send appointment reminders for: " + date, file = 'Send-Log.html')

query = ("SELECT appointment.PatNum as Number, AptDateTime as Time, patient.WirelessPhone as Phone, patient.TxtMsgOk as Txt FROM appointment INNER JOIN patient on appointment.PatNum=patient.PatNum WHERE DATE(AptDateTime) = DATE('" + date + "') AND AptStatus = 1 ORDER BY Time;")
cursor.execute(query)
print "Patients Acquired"

for patient in cursor:
    if patient[3] == 1:
        if patient[2] != '':
            if patient[1].strftime('%p') == 'PM' or int(patient[1].strftime('%I')) >= reminder_hour:
                patient_cell_number.append(patient[2])
                patient_appointment_time.append(patient[1])


x = 0
for number in patient_cell_number:
    appt_time = patient_appointment_time[x].strftime('%I:%M %p')
    msg = "This is a automated reminder of your appointment today scheduled for " + appt_time + " at " + address + " Please text back 'Yes' or call us at " + callbacknumber + " to confirm."
    print 'Sending reminder # ' + str(x + 1) + " of " + str(len(patient_cell_number))
    try:
        text.msg(number, msg)
        log.write("Reminder Sent - Cell Number: " + number + " Time: " + patient_appointment_time[x].strftime('%I:%M %p'), file = 'Send-Log.html')
    except Exception as ex:
        log.write("Reminder Failure - Cell Number: " + number + " Time: " + patient_appointment_time[x].strftime('%I:%M %p') + ' Exception: ' + ex, file = 'Send-Log.html')

#Wait a second between requests to be nice to twilio
    time.sleep(send_delay)
    x += 1
print "Patient reminders sent"
log.write(str(x) + ' patient reminders have been sent. Waiting ', file = 'Overall.html')

#Send out email alerts if enabled.
if email_logs:
    log.email(file = 'Overall.html')
    log.email(file = 'Recived-Log.html')
time.sleep(wait_on_close)
