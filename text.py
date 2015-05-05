from twilio.rest import TwilioRestClient
import configuration

#configuration gets the config.ini from the hard drive and loads it for twilio to use, this depends on the twilio python module.

def send_sms(sid, token, sender, recipient, message):
    account_sid = sid
    auth_token = token
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to=recipient, from_=sender, body=message)


def msg(recipient, message):
    send_sms(configuration.sid(), configuration.auth(), configuration.number(), recipient, message)

