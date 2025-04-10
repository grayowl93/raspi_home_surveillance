import RPi.GPIO as GPIO
import time

print("test start")

door_sw = 17
red_sw = 22
IR_sensor = 27
LED_red = 23
LED_door = 24
LED_IR = 25
Buzzer = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(door_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(red_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_red, GPIO.OUT)
GPIO.setup(LED_door, GPIO.OUT)
GPIO.setup(LED_IR, GPIO.OUT)

GPIO.setup(Buzzer,GPIO.OUT)
pwm = GPIO.PWM(Buzzer,477)

counter = 50

while counter > 0:
	sw = GPIO.input(door_sw)
	GPIO.output(LED_door,sw)
	if 1 == sw:
		print("door open")
	else:
		print("door close")
	sw = GPIO.input(red_sw)
	GPIO.output(LED_red,sw)
	if 1 == sw:
		print("red button ON")
	else:
		print("red button OFF")
	sw = GPIO.input(IR_sensor)
	GPIO.output(LED_IR,sw)
	if 1 == sw:
		print("IR Off")
	else:
		print("IR On")

	counter = counter - 1
	
	time.sleep(1)

GPIO.cleanup(door_sw)
GPIO.cleanup(red_sw)
GPIO.cleanup(IR_sensor)
GPIO.cleanup(LED_red)
GPIO.cleanup(LED_door)
GPIO.cleanup(LED_IR)
GPIO.cleanup(Buzzer)

print("test end.")

