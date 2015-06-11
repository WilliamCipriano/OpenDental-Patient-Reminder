import graph
import mysql.connector

config = {
  'user': 'root',
  'password': '',
  'host': '192.168.6.120',
  'database': 'opendental',
  'raise_on_warnings': True,
}

def AppointmentView():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("""SELECT DATE(AptDateTime) as date FROM appointment
              WHERE DATE(AptDateTime) > CURDATE() AND DATE(AptDateTime)
              < CURDATE() + INTERVAL 180 DAY AND AptStatus NOT IN (7,8,9) ORDER BY 
              AptDateTime""")
    cursor.execute(query)
    results = cursor.fetchall()
    current_date = None
    dates = list()
    numbers = list()
    x = 0
    for result in results:
        if current_date == None:
            current_date = result[0]
            dates.append(result[0].strftime('%a - %m/%d'))
            numbers.append(1)
        if result[0] > current_date:
            x += 1
            current_date = result[0]
            dates.append(result[0].strftime('%a - %m/%d'))
            numbers.append(1)
        else:
            numbers[x] += 1
    
    
    return graph.ClassicBar('Future appointment projections', 'Date', 'Patients', dates, numbers, 750, 3000)
            
def IncomeByCarrier():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("""SELECT CarrierName, SUM(CheckAmt) AS $Income
             FROM claimpayment
             WHERE CheckDate >= CURDATE() - INTERVAL 90 DAY
             AND CheckDate < CURDATE()
             GROUP BY CarrierName""")
    cursor.execute(query)
    results = cursor.fetchall()
    totalcash = list()
    carrier = list()
    for result in results:
        totalcash.append(result[1])
        carrier.append(result[0].replace("'", ""))

    return graph.ClassicBar('Income by carrier (Last 90 days)', 'Carrier', 'Income', carrier, totalcash, 1200, 3000)


def TodaysPayments():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("""SELECT payment.PayDate,patient.ChartNumber,
             CONCAT(patient.FName,' ',patient.LName) AS plfname,
             payment.PayType,payment.CheckNum,payment.PayAmt
             FROM payment,patient
             WHERE payment.PatNum = patient.PatNum
             && payment.PayAmt > 0
             && payment.PayDate = CURDATE()""")
    cursor.execute(query)
    results = cursor.fetchall()
    patientname = list()
    payment = list()
    for result in results:
        if result[3] == 71:
            patientname.append('Credit: ' + result[2])
            payment.append(result[5])
        else:
            patientname.append('Cash: ' + result[2])
            payment.append(result[5])

    return graph.ClassicBar('Cash Payments Made Today', 'Patient', 'Payment', patientname, payment, 1200, 1000)


def YesterdaysPayments():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("""SELECT payment.PayDate,patient.ChartNumber,
             CONCAT(patient.FName,' ',patient.LName) AS plfname,
             payment.PayType,payment.CheckNum,payment.PayAmt
             FROM payment,patient
             WHERE payment.PatNum = patient.PatNum
             && payment.PayAmt > 0
             && payment.PayDate = CURDATE() - 1""")
    cursor.execute(query)
    results = cursor.fetchall()
    patientname = list()
    payment = list()
    for result in results:
        if result[3] == 71:
            patientname.append('Credit: ' + result[2])
            payment.append(result[5])
        else:
            patientname.append('Cash: ' + result[2])
            payment.append(result[5])

    return graph.ClassicBar('Cash Payments Made Yesterday', 'Patient', 'Payment', patientname, payment, 1200, 1000)

