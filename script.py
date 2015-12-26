import requests
import os
import configparser
from twisted.internet import task
from twisted.internet import reactor
from twilio.rest import TwilioRestClient

CURRENT_IP = ''

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
    global CURRENT_IP

    ip = getCurrentIp()
    print(ip)
    if ip != CURRENT_IP:
        sendIpSMS(ip)
        CURRENT_IP = ip

l = task.LoopingCall(checkIp)
l.start(60)
reactor.run()
