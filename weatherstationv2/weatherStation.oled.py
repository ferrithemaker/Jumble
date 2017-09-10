#!/usr/bin/python

import sys
import time

import Adafruit_DHT


import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306


import Adafruit_MCP3008

import Adafruit_BMP.BMP085 as BMP085

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

import urllib2

# MCP3008 config

CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


# OLED i2C Configuration

RST = None     # on the PiOLED this pin isnt used

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
sendtime = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

while True:	
	# Read DHT22 data
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
	
	# BMP180 read data

	bmpsensor = BMP085.BMP085()
	
	# read LDR data
	LDRvalue = mcp.read_adc(0)

	# Draw a black filled box to clear the image.
	draw.rectangle((0,0,width,height), outline=0, fill=0)

	if humidity is not None and temperature is not None:
		#print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		t = str("{0:.2f}".format(temperature))
		h = str("{0:.2f}".format(humidity))
		p = str("{0:.2f}".format(bmpsensor.read_pressure()/100.0))
		l = str(LDRvalue)
		# Write two lines of text.
		draw.text((x, top),       "Temperature: " + t,  font=font, fill=255)
		draw.text((x, top+8),     "Humidity:" + h, font=font, fill=255)
		draw.text((x, top+16),    "Pressure:" + p, font=font, fill=255)
		draw.text((x, top+24),    "Light:" + l, font=font, fill=255)

	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)
		
	#print sendtime
	if sendtime == 60:
		print "http://makersacademy.cat/weatherstation/adddata.php?t="+t+"&h="+h+"&p="+p+"&l="+l
		content=urllib2.urlopen("http://makersacademy.cat/weatherstation/adddata.php?t="+t+"&h="+h+"&p="+p+"&l="+l, timeout = 5)
		sendtime = 0

    

    # Display image.
	disp.image(image)
	disp.display()
	time.sleep(1)
	sendtime = sendtime + 1





