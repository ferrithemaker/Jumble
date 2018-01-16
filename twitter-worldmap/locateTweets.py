#!/usr/bin/python

from __future__ import absolute_import, print_function

import os
from subprocess import call
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import threading
import time
import pygame
import sys
from neopixel import *


pygame_screen_x=800
pygame_screen_y=400

# set up pygame
pygame.init()
pygame.font.init()

pyfont = pygame.font.SysFont("freemono",30)

# print (pygame.font.get_fonts())
# set up the window
windowSurface = pygame.display.set_mode((pygame_screen_x, pygame_screen_y))
pygame.display.set_caption('Maker World Trends')



tweetstring = ""
tweetfrom = ""
continent = ""


continentsandcities = []


with open("worldcities.csv") as continentsandcitiesfile:
	for line in continentsandcitiesfile:
		continentsandcities.append(line.split(","))


script_path = os.path.dirname(os.path.realpath(__file__))


# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=""
consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=""
access_token_secret=""

# This is the string to search in the twitter feed
# May be  a word, an #hashtag or a @username

search_strings = ['makerspace','arduino','raspberry pi','#raspberrypi','esp8266','ESP8266','tinkering','Raspberry Pi','Raspberry pi','Raspberry PI','Arduino','raspberry PI']

class StdOutListener(StreamListener):
    """
    A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
		global tweetstring
		global tweetfrom
		global continent
		global continentsandcities
		continent = ""
		len_continent = 0
		data  = json.loads(data)
		if data['user']['location'] is not None:
			for element in continentsandcities:
				if element[0].encode('utf-8').lower() in data['user']['location'].encode('utf-8').lower() or element[1].encode('utf-8').lower() in data['user']['location'].encode('utf-8').lower() or ((element[2].encode('utf-8').lower() in data['user']['location'].encode('utf-8').lower()) and element[2].encode('utf-8') != ""):
					if len(element[3].encode('utf-8')) > len_continent:
						len_continent = len(element[3].encode('utf-8'))
						continent = element[3].encode('utf-8')
			if continent != "":
				print ("\nContinent: "+continent[:-1])
				tweetstring = data['text'].encode('utf-8')
				tweetfrom =  "Tweet from: "+data['user']['location'].encode('utf-8')
				print (tweetfrom)
				print (tweetstring)
		return True

    def on_error(self, status):
		#print (status)
		return False

def clear(strip,color):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()

def southAmerica(strip,color):
	clear(strip,Color(0,0,0))
	for i in range(0,4):
		strip.setPixelColor(i,color)
	strip.show()
def northAmerica(strip,color):
	clear(strip,Color(0,0,0))
	for i in range(4,9):
		strip.setPixelColor(i,color)
	strip.show()
def europe(strip,color):
	clear(strip,Color(0,0,0))
	for i in range(9,12):
		strip.setPixelColor(i,color)
	strip.show()
def asia(strip,color):
	clear(strip,Color(0,0,0))
	for i in range(12,17):
		strip.setPixelColor(i,color)
	strip.show()
def australia(strip,color):
	clear(strip,Color(0,0,0))
	for i in range(17,22):
		strip.setPixelColor(i,color)
	strip.show()
def africa(strip,color):
	clear(strip,Color(0,0,0))
	for i in range(22,25):
		strip.setPixelColor(i,color)
	strip.show()
        

def show_info():
		# LED strip configuration:
	LED_COUNT      = 25      # Number of LED pixels.
	LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
	#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
	LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
	LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
	LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
	LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
	LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
	LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
	# This is our little animation loop.
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	ev = pygame.event.poll()
	while ev.type!=pygame.QUIT:
		ev = pygame.event.poll()
		textfrom = pyfont.render(tweetfrom,True,(200,200,200))
		textstring = pyfont.render(tweetstring,True,(200,200,200))
		#print (tweetstring)
		windowSurface.fill((0,0,0))
		windowSurface.blit(textfrom,(10,60))
		windowSurface.blit(textstring,(10,100))
		pygame.display.flip()
		#for x in range(255):
		#	windowSurface.fill((0,0,0))
		#	label.set_alpha(255-x)
		#	windowSurface.blit(label,(200,100))
		#	pygame.display.flip()
			#pygame.time.delay(20)
	pygame.quit()
	sys.exit()
#    scrollphat.set_brightness(2)
#    while True:
#         try:
#             scrollphat.scroll()
#             time.sleep(0.1)
#         except KeyboardInterrupt:
#             scrollphat.clear()
#             sys.exit(-1)
             


if __name__ == '__main__':
    s = threading.Thread(target=show_info)
    s.start()
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=search_strings)

