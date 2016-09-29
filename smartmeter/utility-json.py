#!/usr/bin/env python3.4
# Depends:
# netcat, rtlamr, rtl_tcp - https://github.com/bemasher/rtlamr
# 
import subprocess
import socket
import re
import time
import pymysql
import utility_meters
import json
from cloudant.account import Cloudant

USERNAME = '<USERNAME from CLOUDANT>'
PASSWORD = '<PASSWORD from CLOUDANT'
db_name = 'smartmeter'
ACCOUNT_NAME = USERNAME

logfile = "/tmp/copyofstream.txt"
pkt = ''
meters              = {}
electricMeterTypes  = [4, 5, 7, 8]
gasMeterTypes       = [2, 9, 12]
waterMeterTypes     = [11, 13]

logfile = open(logfile,'a')

exec(open("dbConnect.py").read()) # dbConn  = pymysql.connect(user='utility_mon', password='password', host='hostname', database='UtilityMon', autocommit=True)
dbCur   = dbConn.cursor()

# start the rtl device and server
print("Sarting RTL_TCP Out Port 5566")
rtl_tcp = subprocess.Popen("/usr/local/bin/rtl_tcp -p 5566", stdout=subprocess.PIPE, shell=True) # have to manually start it ???
print("sleeping 15 seconds")
time.sleep(15)

print("Sarting RTLAMR In Port 5566; Out on 5577")
print("starting rtlamr")
rtlamr = subprocess.Popen("rtlamr -quiet=true -format=json -unique=true -duration=14m10s -server 127.0.0.1:5566 | /bin/nc -l -p 5577", stdout=subprocess.PIPE, shell=True)
print("sleeping 5 seconds")
time.sleep(5)

rtlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rtlSocket.connect(('127.0.0.1', 5577))

while True:
 pkt = ''
 try:
  newchar = rtlSocket.recv(1)
  while (newchar != '\n'):
   pkt = pkt + newchar
     #pkt = rtlSocket.recv(111).decode("ascii")
   if (newchar != '\n'):
    newchar = rtlSocket.recv(1) # recieve '\n'

  data = json.loads(pkt)
  data['Time'] = time.mktime(time.strptime(data['Time'][:24], "%Y-%m-%dT%H:%M:%S.%f"))
  client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME)
  client.connect()
  session = client.session()
  my_database = client[db_name]

  data.pop('Offset')
  data.pop('Length')
  data['Message'].pop('TamperPhy')
  data['Message'].pop('TamperEnc')
  data['Message'].pop('ChecksumVal')

  logfile.write(str(data))
  logfile.write("\n")
 
  my_document = my_database.create_document(data)

  # Disconnect from the account
  client.disconnect()

 except AttributeError:
  print "There was an error"
  continue
