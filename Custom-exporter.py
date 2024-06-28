import requests
from prometheus_client import start_http_server, Summary ,Gauge
import os
import time
import socket
from dotenv import load_dotenv
from pathlib import Path
import json
import imaplib
import ssl
import subprocess
import pycurl
port = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP=s.getsockname()[0]
request_contract = ["url","cookie"=="","header","body"]

def prom_gauge_post(address,json_cookie,json_header,json_body):

    if  json_cookie == "null":
        json_cookie = ""
        response = requests.post(address, headers=json_header,cookies=json_cookie,json=json_body, verify=False)
        response_code = response.status_code
        return response_code
    if json_body == "null":
        json_body = ""
        response = requests.post(address, headers=json_header,cookies=json_cookie,verify=False)
        response_code = response.status_code
    else:
    response = requests.post(address, cookies=json_cookie, headers=json_header, json=json_body, verify=False)
    response_code = response.status_code
    return response_code

def prom_gauge_get(address):
        response = requests.get(address,verify=False)
        response_code = response.status_code
        return response_code

    #return response.headers

def read_liner(filename,line):
    f = open(filename,"r+")
    line_num = f.readlines(int(line))
    for i in line_num:
        a = i.strip('[')
        b = a.strip('[')
    return b
def read_liner_seprator(filename,line):
    f = open(filename,"r+")
#    g = line - 1
    line_num = f.readlines()[line:line + 1]
    for i in line_num:
        a = i.strip("\n")
    return a

def file_line(filename):
    with open(filename,'r') as fp:
        for count , line in enumerate(fp):
            count_line =  count + 1
    return count_line

def merge_lists(list_one,list_two):
    merged_list = zip(list_one,list_two)
    return merged_list

def launch_gauge(name,output):
    g = Gauge(name, name)
    g.dec(output)

################################################################################

file_names  = ["url","cookie","header", "body","name"]
#file_names  = ["url","header", "body","name"]
file_line(file_names[0])
for e in range(0,file_line(file_names[0])):
    print("first for", e)
    requests_objects = {}
    count_for_two = 0
#    print('this is oprator', file_line(file_names[0]))
    for i in file_names:
        count_for_one = 0
        count_for_one = count_for_one + 1
        requests_objects.update({i: read_liner_seprator(i,e)})
       # print(requests_objects,"e",i,e)

   # method = print(requests_objects.get('method'))
    url = print(requests_objects.get("url"))
    header = requests_objects['header']
    cookie = requests_objects.get("cookie")
    body = requests_objects.get("body")
    name = requests_objects.get("name")
    payload_json = json.dumps(body)
