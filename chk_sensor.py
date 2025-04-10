import RPi.GPIO as GPIO
import time

print("test start")

gpio_sw= 4

GPIO.setmode(GPIO.BCM)

GPIO.setup(gpio_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 50

while counter > 0:
	sw = GPIO.input(gpio_sw)
	if 1 == sw:
		print("open")
	else:
		print("close")
	counter = counter - 1
	time.sleep(1)

GPIO.cleanup(gpio_sw)

print("test end.")

