import RPi.GPIO as GPIO
import string
import time
import datetime
import dateutil
from dateutil.relativedelta import relativedelta
import boto3
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate
#import sendGmail
#import sendShortMessage
#from multiprocessing import Process

port_door_sw = 17
port_red_sw = 22
port_IR_sensor = 27
port_LED_red = 23
port_LED_door = 24
port_LED_IR = 25
port_Buzzer = 18

def surveillance_start_setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(port_door_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(port_red_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(port_IR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(port_LED_red, GPIO.OUT)
	GPIO.setup(port_LED_door, GPIO.OUT)
	GPIO.setup(port_LED_IR, GPIO.OUT)
	GPIO.setup(port_Buzzer,GPIO.OUT)
	pwm = GPIO.PWM(port_Buzzer,477)

def surveillance_end_clean():
	GPIO.cleanup(port_door_sw)
	GPIO.cleanup(port_red_sw)
	GPIO.cleanup(port_IR_sensor)
	GPIO.cleanup(port_LED_red)
	GPIO.cleanup(port_LED_door)
	GPIO.cleanup(port_LED_IR)
	GPIO.cleanup(port_Buzzer)

accesskey = ""
secretkey = ""
region = ""

def sendShortMessage(title,msg):
	print("send to iPhone")
	boto3.set_stream_logger()
	try:
		#print("client")
		sns = boto3.client("sns", aws_access_key_id=accesskey, aws_secret_access_key=secretkey, region_name=region)	
		#print("publish")
		response = sns.publish(PhoneNumber = "",Subject = title,Message = msg)
		#print("response")
	except Exception as err:
		print(err.code)

def sendMsg_eMail(from_address, to_address, cc_address, subject, body, encode):
#	gmail_addr=from_address
	gmail_pass=""
	SMTP="smtp.gmail.com"
	PORT=587
#	from_addr= gmail_addr
#	to_addr="grayowl93@yahoo.co.jp"
#	subject="zushi pi"
#	body="test send"
	msg=MIMEText(body,"plain",encode)
	msg["From"]=from_address
	msg["To"]=to_address
	msg["Subject"]=Header(subject, encode)

	try:
		print("mail Sending now...")
		send = smtplib.SMTP(SMTP,PORT)
#		send.set_debuglevel(True)
		send.ehlo()
		send.starttls()
		send.ehlo()
		send.login(from_address,gmail_pass)
		send.send_message(msg)
		send.close()
	except Exception as e:
		print("except: "+str(e))
	else:
		print("{0} send message.".format(to_address))

def get_door_sw():
	sw = GPIO.input(port_door_sw)
	door_open = False
	if sw == 1:
		door_open = True
	return door_open

def door_LED_on(on):
	if on == True:
		GPIO.output(port_LED_door,1)
	else:
		GPIO.output(port_LED_door,0)
		
def get_Red_sw():
	sw = GPIO.input(port_red_sw)
	Red_on = False
	if sw == 0:
		#print("RED on")
		Red_on = True
	#else:
		#print("RED off")
	return Red_on

def Red_LED_on(on):
	if on == True:
		#print("Red LED on")
		GPIO.output(port_LED_red,1)
	else:
		#print("Red LED off")
		GPIO.output(port_LED_red,0)

def get_IR_sensor():
	sw = GPIO.input(port_IR_sensor)
	print(sw)
	IR_on = False
	if sw == 1:
		IR_on = True
	return IR_on

def IR_LED_on(on):
	if on == True:
		GPIO.output(port_LED_IR,1)
	else:
		GPIO.output(port_LED_IR,0)

if __name__ == "__main__":
	print("test start")
	surveillance_start_setup()
	
	counter = 50000
	cycle_sec = 0
	cycle_min = 0
	emergency = False
	emergency_cycle = 0
	emmergency_cancel_cycle = 0
	door = False
	door_cycle = 0
	door_counter = 0
	IR_Sensor = False
	IR_Sensor_cycle = 0
	IR_Sensor_counter = 0

	
	while counter > 0:
		# 0.1sec----------
		counter = counter - 1

		if get_door_sw() == True:
			door_LED_on(True)
			if door == False:
				door = True
				door_counter = door_counter + 1
		else:
			door_LED_on(False)
			door = False
		if get_IR_sensor() == True:
			IR_LED_on(True)
			if IR_Sensor == False:
				IR_Sensor = True
				IR_Sensor_counter = IR_Sensor_counter + 1
		else:
			IR_LED_on(False)
			IR_Sensor = False
		time.sleep(0.5)
	
	print("test end.")
	surveillance_end_clean()
