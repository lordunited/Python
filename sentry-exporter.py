import requests
import socket
from prometheus_client import start_http_server, Summary ,Gauge
import ssl
import time
import json
import sh
ctx = ssl.create_default_context()
ctx.set_ciphers('DEFAULT')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP=s.getsockname()[0]
request_contract = ["url","cookie"=="","header","body"]
def create_gauge(output,name):
    g = Gauge(name, name)    
    g.dec(output)


api_key = "your_api_key"

url = "https://#YOURURL/api/0/projects/sentry/boomcore/events/"

headers_sentry = {
    'Authorization': 'YOUR TOKEN',
}
response_sentry = requests.get(url, headers=headers_sentry)
print(response_sentry.content)
with open("json_file", 'w') as j:
    j.write(str(response_sentry.content))
start_http_server(addr=IP,port=8001)
while True:
    time.sleep(40)
