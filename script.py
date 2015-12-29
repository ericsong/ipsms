import requests
import os
import configparser
import sched, time
from twilio.rest import TwilioRestClient

config = configparser.ConfigParser()
config.read('config.ini')

account = config['TWILIO']['ACC']
token = config['TWILIO']['TOKEN']
client = TwilioRestClient(account, token)

def getCurrentIp():
    r = requests.get('http://icanhazip.com')
    ip = r.text.strip()
    return ip

def sendIpSMS(ip):
    numbers = config['PHONE_NUMBERS']['TO'].split(",")

    for number in numbers:
        message = client.messages.create(
            to=number,
            from_=config['PHONE_NUMBERS']['FROM'],
            body=ip
        )

def checkIp():
    ip = getCurrentIp()
    print(ip)

    if ip != config['IP']['CURRENT']:
        sendIpSMS(ip)

        config['IP']['CURRENT'] = ip
        with open(r'config.ini', 'wb') as configfile:
            config.write(configfile)

s = sched.scheduler(time.time, time.sleep)
def repeat_task(sc):
    checkIp()
    sc.enter(60, 1, repeat_task, (sc,))

s.enter(60, 1, repeat_task, (s,))
s.run()
