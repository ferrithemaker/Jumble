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


#board=Arduino("/dev/ttyACM0")
#board=Arduino("/dev/ttyUSB0")
board=Arduino("/dev/ttyAMA0")
board.digital[9].mode = SERVO # humidity
board.digital[8].mode = SERVO # temp
board.digital[11].mode = SERVO # light
it = util.Iterator(board)
it.start()
# Start reporting for defined pins
board.analog[3].enable_reporting()


count=0
lastlightvalue=0
light=0
servolightposition=arduino_map((math.sqrt(1024-light)),0,32,10,170)
while True:
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
	if humidity is not None and temperature is not None:
        	time.sleep(1)
		light=board.analog[3].read()
		light=int(light*1000)
        	# light sensor tunning, must be setup always
		if light>1024:
                	light=1024
        	if light<0:
                	light=0
        	servotemp=arduino_map(math.fabs(temperature),0,45,10,170)
        	servohum=arduino_map(math.fabs(humidity),0,100,10,170)
		servolight=math.sqrt(light)
		servolightposition=arduino_map((math.sqrt(light)),0,32,10,170)
        	board.digital[9].write(servohum)
        	board.digital[8].write(servotemp)
		board.digital[11].write(servolightposition)
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
