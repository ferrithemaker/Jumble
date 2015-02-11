#!/usr/bin/env python
 
 
import RPi.GPIO as GPIO, time, os      
import math
from pyfirmata import Arduino, util, SERVO
import sys
import Adafruit_DHT
import subprocess

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
board=Arduino("/dev/ttyACM0")
#board=Arduino("/dev/ttyUSB0")
board.digital[10].mode = SERVO # humidity
board.digital[9].mode = SERVO # temp
board.digital[11].mode = SERVO # light
count=0
while True:
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
	if humidity is not None and temperature is not None:
        	light=RCtime(18)
        	if light>32768:
                	light=32768
        	if light<0:
                	light=0
        	servolightposition=arduino_map(128-math.sqrt(light/2),0,128,10,170)
		#print light
		#print servolightposition
        	#print '{0:0.1f},{1:0.1f}'.format(humidity, temperature)
        	servotemp=arduino_map(math.fabs(temperature),0,45,10,170)
        	servohum=arduino_map(math.fabs(humidity),0,100,10,170)
        	board.digital[10].write(servohum)
        	board.digital[9].write(servotemp)
		board.digital[11].write(servolightposition)
		servolight=arduino_map(128-math.sqrt(light/2),0,128,0,32)
		#print servolight
		# send data online
		count=count+1
		if count==30:
			devnull = open("/dev/null","w")
			datastring="http://www.ferranfabregas.info/weatherstation/addinfo.php?data="+str((time.strftime("%Y%m%d%H%M%S")))+","+str('{0:0.1f}'.format(humidity))+","+str('{0:0.1f}'.format(temperature))+","+str(servolight)
			print datastring
    			subprocess.call(["wget",datastring],stderr=devnull)
			count=0
		time.sleep(2)
