import cx_Oracle
import requests
import json 
import time
import datetime
import logging
from multiprocessing import Process
import os
oracle_quary=""
oracle_user=''
oracle_password=''
oracle_dwh=''

#import dbconfig
#def mattermost_push(url,message):
#    requests.post(url=url,data=message)
class Matterhook:

    def __init__(self):
        self.status_code = None
        self.headers = {'content-type': 'application/json'}

    def post_message(self, url, message_payload, headers=None, timeout=None):
        if not message_payload:
            raise ValueError("Empty message payload provided.")
  #      if not isinstance(message_payload, dict):
   #         raise ValueError("Message payload should be a dictionary.")

        if not url:
            raise ValueError("Empty URL provided.")
        if not isinstance(url, str):
            raise ValueError("URL should be a string.")

        if headers is not None and not isinstance(headers, dict):
            raise ValueError("Headers should be a dictionary.")
        self.headers.update(headers or {})
        try:
            #response = requests.post(url, json=json.dumps(message_payload), headers=self.headers, timeout=timeout)
            response = requests.post(url, json=message_payload, headers=self.headers, timeout=timeout)
            response.raise_for_status()
            self.status_code = response.status_code
        #    return response,response.status_code
        #    return response.stat
        except requests.exceptions.RequestException as e:
            raise e

    def get_status_code(self):
        """
        Return the status code of the last request, or None if no request has been sent.

        :return: The HTTP status code of the last request.
        :rtype: int or None
        """
        return self.status_code
def ORCL_EXECUTER(quary=query_oracle,user="",password="",dsn=""):
    con = cx_Oracle.connect(user=user,password=password,dsn=dsn)
    cursor = con.cursor()
    cursor.execute(quary)
    rows = cursor.fetchall()
    for row in rows:
      final_row = row
    return final_row

now = datetime.datetime.now()

while True:
 if __name__ == '__main__':
  print("main if ")
  ORACL_EXECUTER_OUTPUT = ORCL_EXECUTER(oracle_quary,oracle_user,oracle_password,oracle_dwh)
  p = Process(target=ORCL_EXECUTER)
  p.start()
  p.join()
  print("clock is ", now.hour)
  if ((ORACL_EXECUTER_OUTPUT[0]  != 0) and  (7 < now.hour < 17)):
    print("second if")
    notify = Matterhook()
    dict = {}
    dict_value = ORACL_EXECUTER_OUTPUT
    dict.update(text=json.dumps(ORACL_EXECUTER_OUTPUT))
    print("start sending webhook ")
    print(datetime.datetime.now(),ORACL_EXECUTER_OUTPUT,"=============") 
    notify.post_message('https://mattermost_hook',dict)
    print("webhook sent")
    print(datetime.datetime.now(),ORACL_EXECUTER_OUTPUT,"=============") 
   # print (ORACL_EXECUTER_OUTPUT)
    logging.debug(ORACL_EXECUTER_OUTPUT,"Time is ", now.hour)
    time.sleep(30)
    #time.sleep(30)
    
    print("next sleep")
    pass
  else:
    logging.debug(ORACL_EXECUTER_OUTPUT,"Time is ", now.hour)
    print("out of time")
    time.sleep(300)
    #pass
 print("finish Loop start again")
 
