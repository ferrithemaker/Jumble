#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!
# Modifications by ferran fabregas ferri.fc@gmail.com

import RPi.GPIO as GPIO, time, os      
import math
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

result=RCtime(18);
if result>1024:
	result=1024
if result<0:
	result=0
#result=arduino_map(result,0,200,0,120)
#result=result/4.0

print '%.2f' %(32-math.sqrt(result))
