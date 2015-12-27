import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
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

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "ipsms"
    _svc_display_name_ = "ipsms"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        s = sched.scheduler(time.time, time.sleep)
        def repeat_task(sc):
            checkIp()
            sc.enter(60, 1, repeat_task, (sc,))

        s.enter(60, 1, repeat_task, (s,))
        s.run()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
