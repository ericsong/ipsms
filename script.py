import requests
import os
import configparser
from twisted.internet import task
from twisted.internet import reactor
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
    message = client.messages.create(
        to=config['PHONE_NUMBERS']['TO'],
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

l = task.LoopingCall(checkIp)
l.start(60)
reactor.run()
