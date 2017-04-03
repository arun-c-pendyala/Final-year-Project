
import RPi.GPIO as GPIO
import datetime
import time
import sys
import serial
import gspread
import oauth2client.client
import json
import logging
from apscheduler.scheduler import Scheduler

#explanation of code and setup has been well documented in the project report

logging.basicConfig()

#gpio setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.IN)
elvalue = 0
value = 0
electval = 0
eltemp = 0

#json filename for credentials
JSON_FILENAME = 'Energy meter-1353d119396a.json'

#Google sheet to save to

GSHEET_NAME = 'Energy meter readings'

#load credentials from json and open the spreadsheet for writing

json_key = json.load(open(JSON_FILENAME))
creds = oauth2client.client.SignedJwtAssertionCredentials(json_key['client_email'],json_key['private_key'],['https://spreadsheets.google.com/feeds'])
client_inst = gspread.authorize(creds)
gsheet = client_inst.open(GSHEET_NAME).sheet1

#start the scheduler
sched = Scheduler()
sched.daemonic = False

#schedules job to be run once each minute
@sched.interval_schedule(minutes=1, misfire_grace_time = 15)

def job_function():
	global elvalue
	global eltemp
	global elvalue2
	elvalue2 = elvalue - eltemp  # current month consumption is given by the difference between total value and previous month consumption
	eltemp = elvalue   
	global electval
	electval = float(elvalue2)/3200
	print(elvalue2)
	print(datetime.datetime.now())
	curr_time = datetime.datetime.now()
	print "Writing new row to %s : %s - %3.1f - %f " %(GSHEET_NAME,curr_time,elvalue2,electval)

	gsheet.append_row((curr_time,elvalue2,electval))

	ser = serial.Serial('/dev/ttyAMA0',9600,timeout = 1) # code for gsm module
	ser.open()
	time.sleep(3)
	ser.write('Your Monthly statement of energy consumption (in KWH) :')
	ser.write(str(electval))
	time.sleep(3)
	ser.write(chr(26))
	ser.close()

while(True):  # count the number of pulses
	prevval = value 
	value = GPIO.input(7)
	if(value==0 and value != prevval):
		elvalue = elavalue +1
	else:
		pass
