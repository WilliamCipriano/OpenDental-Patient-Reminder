from flask import Flask, request, redirect
import twilio.twiml
import log
import mysql.connector
from datetime import datetime

#Checks for a Y or Yes response from the patient
def CheckForYes(string):
    string = string.lstrip(' ')[:3]
    if string == 'Yes':
        return True
    if string == 'YES':
        return True
    if string == 'yES':
        return True
    if string == 'yes':
        return True
    if string == 'y':
        return True
    if string == 'Y':
        return True
    return False


#MySql configuration for OpenDental
config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'database': 'opendental',
  'raise_on_warnings': True,
}
 
#This runs on flask, it is a modified version of twilio's example
app = Flask(__name__)
 
 
@app.route("/", methods=['GET', 'POST'])
def text_responder():

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
 
    fromnum = request.values.get('From', None)
    body = request.values.get('Body', None)

    if CheckForYes(body): 
        num = fromnum[2:]
        num = '(' + num[:3] + ')' + num[3:6] + '-' + num[6:10]
        try:
            #see if patient exists
            query = ("SELECT AptNum, patient.PatNum, patient.WirelessPhone FROM appointment INNER JOIN patient on appointment.PatNum=patient.PatNum WHERE date(AptDateTime) = CURDATE() and WirelessPhone = '" + str(num) + "'")
            cursor.execute(query)
            result = cursor.fetchone()
        except Exception as ex:
            log.write('Database Error:' + str(ex), file = 'Recived-Log.html')
        try:
            #confirm the appointment if he does
            confirmnote = "Confirmed automatically at: " + datetime.now().strftime('%I:%M %p')
            query = ("UPDATE appointment SET Confirmed = 21 WHERE AptNum = " + str(result[0]))
            cursor.execute(query)
            query = ("UPDATE appointment SET note = if(note = '', '" + confirmnote + "', concat(note, '\n" + confirmnote + "'))")
            cursor.execute(query)
            message = "Your appointment has been confirmed."
        except Exception as ex:
            log.write('Database Error:' + str(ex), file = 'Recived-Log.html')
        log.write('Appointment confirmed for patient number: ' + str(result[1]), file = 'Recived-Log.html')
    else:
        message = "I'm sorry, I didn't get that. Please send Yes to confirm or call to cancel."
        log.write('Confirm failed with message: ' + body, file = 'Recived-Log.html')
        
    resp = twilio.twiml.Response()
    resp.message(message)
 
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
