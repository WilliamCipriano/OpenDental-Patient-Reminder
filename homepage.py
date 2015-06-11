import mysql.connector

config = {
  'user': 'root',
  'password': '',
  'host': '192.168.6.120',
  'database': 'opendental',
  'raise_on_warnings': True,
}

def GetAppointmentCount(days = 0):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("""SELECT COUNT(AptNum) from Appointment
             WHERE DATE(AptDateTime) BETWEEN CURDATE() - INTERVAL """ + str(days) +
             """ DAY AND CURDATE() AND AptStatus NOT IN (7,8,6)""")
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0]

def GetCompletedAppointmentCount(days = 0):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("""SELECT count(AptNum) from Appointment
             WHERE DATE(AptDateTime) BETWEEN CURDATE() - INTERVAL """ + str(days) +
             """ day AND CURDATE() AND AptStatus = 2""")
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0]

def GetBrokenAppointments(days = 0):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("""SELECT count(AptNum) from Appointment
             WHERE DATE(AptDateTime) BETWEEN CURDATE() - INTERVAL """ + str(days) +
             """ day AND CURDATE() AND AptStatus = 5""")
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0]

def GetProduction(days = 0):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("""SELECT SUM(ProcFee) FROM procedurelog
             WHERE ProcDate BETWEEN CURDATE() - INTERVAL """ + str(days) +
             """ day AND CURDATE() AND ProcStatus = 2""")
    cursor.execute(query)
    result = cursor.fetchone()
    return '{:20,.2f}'.format(result[0])

def GetEmployeesWorkedToday():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("""SELECT count(DISTINCT EmployeeNum)
             FROM clockevent WHERE DATE(TimeEntered1)
             = CURDATE()""")
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] 

def GetHomepageData():
    x = dict()
    x['AppointmentsToday'] = GetAppointmentCount()
    x['CompletedAppointmentsToday'] = GetCompletedAppointmentCount()
    x['BrokenAppointmentsToday'] = GetBrokenAppointments()
    x['ProductionToday'] = GetProduction()
    x['EmployeesWorked'] = GetEmployeesWorkedToday()
    x['Appointments30days'] = GetAppointmentCount(days = 30)
    x['CompletedAppointments30'] = GetCompletedAppointmentCount(days = 30)
    x['BrokenAppointments30'] = GetBrokenAppointments(days = 30)
    x['Production30'] = GetProduction(days = 30)
    x['Appointments365days'] = GetAppointmentCount(days = 365)
    x['CompletedAppointments365'] = GetCompletedAppointmentCount(days = 365)
    x['BrokenAppointments365'] = GetBrokenAppointments(days = 365)
    x['Production365'] = GetProduction(days = 365)
    return x
    
