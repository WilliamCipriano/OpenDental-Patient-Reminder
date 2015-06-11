import mysql.connector
from datetime import datetime, timedelta
import time
import text
import time
import datetime
import log
import persistentlist

#Written by: Will Cipriano, willcipriano.com


#Variables
delta24h = timedelta(hours=13)
date = time.strftime("%Y-%m-%d")
today = datetime.date.today()
campaign_name = 'LibertyTest1'

#How many seconds to wait between messages.
send_delay = 1

#Define database location and information here, if you are paranoid you can compile this to a .pyc to prevent a casual attacker.
config = {
  'user': 'root',
  'password': '',
  'host': '192.168.6.120',
  'database': 'opendental',
  'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

log.write("\n Beginning to send patient reactivation messages: " + date, file = 'Overall.html')

date = '2014-05-01'

query = ("SELECT patient.PatNum,patient.WirelessPhone,patient.TxtMsgOk,patient.LName,patient.FName,MAX(procedurelog.ProcDate) FROM patient,procedurelog WHERE procedurelog.PatNum=patient.PatNum AND procedurelog.ProcStatus = '2' GROUP BY procedurelog.PatNum HAVING MAX(ProcDate) < '" + date + "';")
cursor.execute(query)
patients = cursor.fetchall()

persistentlist.Load(campaign_name)

y = 0
n = 0

x = 0

for patient in patients:
    if patient[2] == 1:
        query = ("SELECT DATE(MAX(AptDateTime)) from appointment WHERE PatNum = " + str(patient[0]))
        cursor.execute(query)
        last_date = cursor.fetchone()
        if last_date[0] != None:
            if last_date[0] < today:
                if not persistentlist.CheckItem(str(patient[0])) :
                    if x < 200:
                        if patient[1] != '':
                            persistentlist.AddItem(patient[0])
                            log.write("text message sent to patient number: " + str(patient[0])) 
                            print str(patient[1] + ' msg sent!')
                            y += 1
                            x += 1
                else:
                    print str(patient[1] + ' msg skipped!')
                    n += 1
persistentlist.Save()

print "Total y:" + str(y)
print "Total n:" + str(n)
    
  
