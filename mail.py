import smtplib

#Can't be named 'email.py'

#Creds
from_address = '?'
username = '?'
password = '?'

def email(recipient, message, subject):
    global username
    global password
    global from_address
    message = 'Subject: %s\n\n%s' % (subject, message)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(from_address, recipient, message)
    server.quit()

email('alldentex@gmail.com', 'test', 'test')
