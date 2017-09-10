#!/usr/bin/python



from __future__ import division


import sys
import time
import math
import smbus

import Adafruit_DHT


import Adafruit_GPIO.SPI as SPI

import Adafruit_MCP3008

import Adafruit_BMP.BMP085 as BMP085

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

import urllib2

def arduino_map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


# TSL2561 address, 0x39(57) (sensor de LUX)
# Select control register, 0x00(00) with command register, 0x80(128)
#		0x03(03)	Power ON mode

# Get I2C bus
bus = smbus.SMBus(1)

bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
# TSL2561 address, 0x39(57)
# Select timing register, 0x01(01) with command register, 0x80(128)
#		0x02(02)	Nominal integration time = 402ms
bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

time.sleep(1)        
        
# Import the PCA9685 module.
#import Adafruit_PCA9685


#def set_servo_pulse(channel, pulse):
#    pulse_length = 1000000    # 1,000,000 us per second
#    pulse_length //= 60       # 60 Hz
#    print('{0}us per period'.format(pulse_length))
#    pulse_length //= 4096     # 12 bits of resolution
#    print('{0}us per bit'.format(pulse_length))
#    pulse *= 1000
#    pulse //= pulse_length
#    pwm.set_pwm(channel, 0, pulse)

# Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685()

# Set frequency to 60hz, good for servos.
#pwm.set_pwm_freq(60)

# Configure min and max servo pulse lengths
#servo_min = 150  # Min pulse length out of 4096
#servo_max = 600  # Max pulse length out of 4096


# MCP3008 config

#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)



sendtime = 0

while True:	
	# Read DHT22 data
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
	
	# BMP180 read data

	bmpsensor = BMP085.BMP085()
	
	# read LDR data
	#LDRvalue = mcp.read_adc(0)
		
	# Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
	# ch0 LSB, ch0 MSB
	data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)

	# Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
	# ch1 LSB, ch1 MSB
	data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)

	if humidity is not None and temperature is not None:
		
		#print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		
		# Convert the data
		luxtotal = data[1] * 256 + data[0]
		luxIR = data1[1] * 256 + data1[0]
		luxVISIBLE = luxtotal - luxIR
		
		t = str("{0:.2f}".format(temperature))
		h = str("{0:.2f}".format(humidity))
		p = str("{0:.2f}".format(bmpsensor.read_pressure()/100.0))
		lT = str(luxtotal)
		lIR = str(luxIR)
		lVIS = str(luxVISIBLE)
		#l = str(LDRvalue)
		
		# servo mapping
		
		#servotemp=arduino_map(math.fabs(temperature),0,45,servo_min+10,servo_max-10)
		#servohum=arduino_map(math.fabs(humidity),0,100,servo_min+10,servo_max-10)
		#servolight=arduino_map(LDRvalue,0,1023,servo_min+10,servo_max-10)
		#servobar=arduino_map(bmpsensor.read_pressure()/100.0,950,1050,servo_min+10,servo_max-10)
		#if luxtotal>1000:
		#	luxtotal=1000
		#servolux=arduino_map(luxtotal,0,1050,servo_min+10,servo_max-10)
		#pwm.set_pwm(0, 0, int(servotemp))
		#pwm.set_pwm(1, 0, int(servohum))
		#pwm.set_pwm(2, 0, int(servolight))
		#pwm.set_pwm(2, 0, int(servolux))
		#pwm.set_pwm(3, 0, int(servobar))
		
		
		sendtime = sendtime +1
		print sendtime
		if sendtime == 2:
			#print "http://garageofinventors.tech/weatherstation/adddata.php?t="+t+"&h="+h+"&p="+p+"&lir="+lIR+"&lvis="+lVIS
			content=urllib2.urlopen("http://garageofinventors.tech/weatherstation/adddata.php?t="+t+"&h="+h+"&p="+p+"&lir="+lIR+"&lvis="+lVIS, timeout = 5)
			sendtime = 0
	else:
		print "ERROR DHT22"	
	time.sleep(30)
	






