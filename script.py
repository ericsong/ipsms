import requests

r = requests.get('http://icanhazip.com')
ip = r.text.strip()

print(ip)
