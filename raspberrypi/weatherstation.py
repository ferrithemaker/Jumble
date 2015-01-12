#!/usr/bin/env python
 
 
import RPi.GPIO as GPIO, time, os      
import math
from pyfirmata import Arduino, util, SERVO
import sys
import Adafruit_DHT

DEBUG = 1
GPIO.setmode(GPIO.BCM)


def arduino_map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def RCtime (RCpin):
        reading = 0
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(RCpin, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
        while (GPIO.input(RCpin) == GPIO.LOW):
                reading += 1
        return reading
#board=Arduino("/dev/ttyACM0")
board=Arduino("/dev/ttyUSB0")
board.digital[10].mode = SERVO # humidity
board.digital[9].mode = SERVO # temp
board.digital[11].mode = SERVO # light

while True:
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
	if humidity is not None and temperature is not None:
        	light=RCtime(22)
        	if light>1024:
                	light=1024
        	if light<0:
                	light=0
        	servolightposition=arduino_map(32-math.sqrt(light),0,32,0,180)
		print servolightposition
        	print '{0:0.1f},{1:0.1f}'.format(humidity, temperature)
        	servotemp=arduino_map(math.fabs(temperature),0,45,0,180)
        	servohum=arduino_map(math.fabs(humidity),0,100,0,180)
        	board.digital[10].write(servohum)
        	board.digital[9].write(servotemp)
		board.digital[11].write(servolightposition)
		time.sleep(2)
