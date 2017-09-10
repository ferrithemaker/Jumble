#!/usr/bin/python

import sys
import time

import Adafruit_DHT


import Adafruit_GPIO.SPI as SPI

import Adafruit_MCP3008

import Adafruit_BMP.BMP085 as BMP085


import subprocess
import urllib2

# MCP3008 config

CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


	
# Read DHT22 data
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)

# BMP180 read data

bmpsensor = BMP085.BMP085()

# read LDR data
LDRvalue = mcp.read_adc(0)


if humidity is not None and temperature is not None:
	#print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
	t = str("{0:.2f}".format(temperature))
	h = str("{0:.2f}".format(humidity))
	p = str("{0:.2f}".format(bmpsensor.read_pressure()/100.0))
	l = str(LDRvalue)
	print "http://makersacademy.cat/weatherstation/adddata.php?t="+t+"&h="+h+"&p="+p+"&l="+l
	content=urllib2.urlopen("http://makersacademy.cat/weatherstation/adddata.php?t="+t+"&h="+h+"&p="+p+"&l="+l, timeout = 5)
else:
	print('Failed to get reading. Try again!')
	sys.exit(1)










