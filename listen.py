from flask import Flask, request, redirect, make_response, render_template
import twilio.twiml
import log
import mysql.connector
import datetime
import chartgen
import os
import homepage
from collections import Counter

user_tokens = list()

#Local Path
try:
    localpath = os.path.dirname(os.path.abspath(__file__)).replace('\\library.zip','')
except NameError:  # We are the main py2exe script, not a module
    import sys
    localpath = os.path.dirname(os.path.abspath(sys.argv[0])).replace('\\library.zip','')

#Simple user verfication based on a cookie and random token
#for local network use only
def token_gen():
    import random
    import string
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(100))

def user_verification(token):
    if token in user_tokens:
        return True
    else:
        return False

#Checks for a Y or Yes response from the patient
def CheckForYes(string):
    string = string.lstrip(' ')[:3]
    if string == 'Yes':
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
  'host': '192.168.6.120',
  'database': 'opendental',
  'raise_on_warnings': True,
}

app = Flask(__name__, static_url_path='/static/')
 
 
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
            query = ("UPDATE appointment SET Confirmed = 21 WHERE AptNum = " + str(result[0]))
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

@app.route("/chart/<chart>", methods=['GET'])
def chart_responder(chart):
    if chart == 'appointmentview':
        return chartgen.AppointmentView()
    if chart == 'incomebycarrier':
        return chartgen.IncomeByCarrier()
    if chart == 'todayspayments':
        return chartgen.TodaysPayments()
    if chart == 'yesterdayspayments':
        return chartgen.YesterdaysPayments()

@app.route("/logs/<log>", methods=['GET'])
def log_responder(log):
    if log == 'sent':
        f = open(localpath + '//logs/Send-Log.html')
        return f.read()
    if log == 'received':
        f = open(localpath + '//logs/Received-Log.html')
        return f.read()

@app.route("/login", methods=['GET'])
def login():
    loginpage = open(localpath + '\static\login.html', 'r')
    return loginpage.read()

@app.route('/loginver', methods=['POST'])
def CheckPassword():
    username = request.form["user"]
    password = request.form["pwd"]
    if os.path.isfile(localpath + "//auth//" + username + ".txt"):
        f = open(localpath + "//auth//" + username + ".txt", 'r')
        stored_password = f.read()
        if password == stored_password:
            token = token_gen()
            response = make_response(redirect('/home'))
            response.set_cookie('token', token)
            user_tokens.append(token)
            return response
    return username + password

@app.context_processor
def HomeLoad():
    return homepage.GetHomepageData()

@app.route('/home', methods=['GET'])
def Home():
    token = request.cookies.get('token')
    if user_verification(token):
        return render_template('home.html')
    else:
        response = make_response(redirect('/login'))
        return response


 
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
