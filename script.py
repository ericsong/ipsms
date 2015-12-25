import requests
import os
import configparser
from twilio.rest import TwilioRestClient

config = configparser.ConfigParser()
config.read('config.ini')

account = config['TWILIO']['ACC']
token = config['TWILIO']['TOKEN']
client = TwilioRestClient(account, token)

r = requests.get('http://icanhazip.com')
ip = r.text.strip()

message = client.messages.create(
    to=config['PHONE_NUMBERS']['TO'],
    from_=config['PHONE_NUMBERS']['FROM'],
    body=ip
)

print(ip)
