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

# set key befor execute.
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
		# set PhoneNumber.
		response = sns.publish(PhoneNumber = "",Subject = title,Message = msg)
		#print("response")
	except Exception as err:
		print(err.code)

def sendMsg_eMail(from_address, to_address, cc_address, subject, body, encode):
#	gmail_addr=from_address
# set pass word.
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
	#print("IR sensor :"+str(sw))
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
	#print("test start")
	surveillance_start_setup()
	
	counter = 2
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

	detect_warrning = 20

	mail_to="grayowl93@yahoo.co.jp"
	mail_from="yardbirds.zushi7541@gmail.com"
	mail_cc="grayowl93@i.softbank.jp"
	mail_subject="zushi report"
	mail_body="test"
	mail_encode="utf-8"

	#p_EM_send = Process(target=sendShortMessage,args=("Emergency","Now"))
	#p_EM_Cancel_send = Process(target=sendShortMessage,args=("Emergency","Cancel!"))
	date_start = datetime.date.today()
	#debug-----
	#date_start = date_start - datetime.timedelta(days=1)
	print("start day:",date_start)

	detect_start = datetime.datetime.now()
	#date_start = date_start + relativedelta(day=+1)
	
	while counter > 0:
		# 0.1sec----------
		if emergency == False:
			if emmergency_cancel_cycle > 0:
				emmergency_cancel_cycle = emmergency_cancel_cycle -1
			else:
				#print("LED buttun check")
				if get_Red_sw() == True:
					print("Em button on!")
					emergency = True
					Red_LED_on(True)
					#p_EM_send.start()
					#p_EM_send.join()
					sendShortMessage("Emergency","Emergency!")
		else:
			if get_Red_sw() == True:
				emergency_cycle = emergency_cycle + 1
				#print("emergency cancel check:",emergency_cycle)
				if emergency_cycle == 20:
					# 2秒秒長押しseconds long push ON
					print("EM long push OK")
					emergency = False
					Red_LED_on(False)
					#p_EM_Cancel_send.start()
					#p_EM_Cancel_send.join()
					sendShortMessage("Emergency","Cancel...")
					emmergency_cancel_cycle = 10
			else:
				emergency_cycle = 0
		# 0.1sec----------
		cycle_sec = cycle_sec + 1
		if cycle_sec == 10:
			cycle_sec = 0;
			# 1sec----------
			if get_door_sw() == True:
				door_LED_on(True)
				if door == False:
					door = True
					door_counter = door_counter + 1
					detect_start = datetime.datetime.now()
					detect_warrning = 20
			else:
				door_LED_on(False)
				door = False
			if get_IR_sensor() == True:
				IR_LED_on(True)
				if IR_Sensor == False:
					IR_Sensor = True
					IR_Sensor_counter = IR_Sensor_counter + 1
					detect_start = datetime.datetime.now()
					detect_warrning = 20
			else:
				IR_LED_on(False)
				IR_Sensor = False
			# 1sec----------
			cycle_min = cycle_min + 1
			if cycle_min == 60:
				cycle_min = 0
				# 1minuteーーーーーー----------
				#print("minute cycle-----")
				#print(detect_start)
				passed_time = detect_start + datetime.timedelta(hours=detect_warrning)
				now_time = datetime.datetime.now()
				#print(detect_start)
				#print(passed_time)
				#print(now_time)
				if now_time > passed_time:
					sendShortMessage("Emergency","20 hours not detect.")
					detect_warrning = detect_warrning + 1;
				#passed_time = detect_start + datetime.timedelta(seconds=detect_warrning)
				#now_time = datetime.datetime.now()
				#print(now_time)
				#print(passed_time)
				#if now_time > passed_time:
					#print("20 hours not detect.")
					#detect_warrning = detect_warrning + 1;
					#print(detect_warrning)
				
				date_now = datetime.date.today()
				if date_start.day != date_now.day:
					print("time",date_start)
					mail_subject = "daily report " + date_start.strftime('%Y/%m/%d')
					mail_body = "freezer door open:" + str(door_counter) + "\nIR sensor        :" + str(IR_Sensor_counter)
					sendMsg_eMail(mail_from, mail_to, mail_cc, mail_subject, mail_body, mail_encode)
					door_counter = 0
					IR_Sensor_counter = 0
					date_start = date_now

				#counter = counter - 1
				# 1minuteーーーーーー----------
		time.sleep(0.1)
	
	print("test end.")
	surveillance_end_clean()
