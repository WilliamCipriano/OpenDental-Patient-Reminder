import mysql.connector
from datetime import datetime, timedelta
import time
import text
import time

#Written by: Will Cipriano, willcipriano.com

#this accesses the OpenDental database and then loads all the patients with appointments for today, then uses text.msg() to send them to the respective phone numbers.
#This depends on the twillo python module as well as mysql.connector.

delta24h = timedelta(hours=13)

date = time.strftime("%Y-%m-%d")

#Will not send reminders to patients scheduled before this time.
reminder_hour = 9



log = ''

#Define database location and information here, if you are paranoid you can compile this to a .pyc to prevent a casual attacker.

config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'database': 'opendental',
  'raise_on_warnings': True,
}



patient_cell_number = []
patient_appointment_time = []

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

log += "\n Begining to send appointment reminders for: " + date + " \n"

query = ("SELECT appointment.PatNum as Number, AptDateTime as Time, patient.WirelessPhone as Phone, patient.TxtMsgOk as Txt FROM appointment INNER JOIN patient on appointment.PatNum=patient.PatNum WHERE DATE(AptDateTime) = DATE('" + date + "') AND AptStatus = 1 GROUP BY Time;")
cursor.execute(query)
print "Patients Aquired"

for patient in cursor:
    if patient[3] == 1:
        if patient[2] != '':
            if patient[1].strftime('%p') == 'PM' or int(patient[1].strftime('%I')) >= reminder_hour:
                patient_cell_number.append(patient[2])
                patient_appointment_time.append(patient[1])

				
x = 0
for number in patient_cell_number:
    appt_time = patient_appointment_time[x].strftime('%I:%M %p')
    log += "Reminder Sent - Cell Number: " + number + " Time: " + patient_appointment_time[x].strftime('%I:%M %p') + " \n"
    msg = "This is a reminder of your appointment today scheduled for " + appt_time + " at Liberty Place 1625 Chestnut St. If you have any questions please don't hesitate to call us at (215)336-8399."
    print 'Sending reminder # ' + str(x + 1) + " of " + str(len(patient_cell_number))
    x += 1
print "Patient reminders sent"    
f = open('log.ini', 'a')
print "Logfile open"
log += "Appointment reminders sent successfully \n"
f.write(log)
print "Logs written"
f.close()
print "Logfile closed"
print "Patient reminders have been sent"
time.sleep(15)
