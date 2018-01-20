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
import random
#import pygame
import sys
from neopixel import *


pygame_screen_x=800
pygame_screen_y=400

# set up pygame
#pygame.init()
#pygame.font.init()

#pyfont = pygame.font.SysFont("freemono",30)

# print (pygame.font.get_fonts())
# set up the window
#windowSurface = pygame.display.set_mode((pygame_screen_x, pygame_screen_y))
#pygame.display.set_caption('Maker World Trends')


tweetstring = ""
tweetfrom = ""
continent = ""
choice = ""

found = False

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

search_strings = ['arduino','raspberry pi','#raspberrypi','Raspberry Pi','Raspberry pi','Raspberry PI','Arduino','raspberry PI','#arduino','#Arduino']

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
		global found
		global choice
		continent = ""
		len_continent = 0
		data  = json.loads(data)
		print ("INCOMMING TWEET!")
		if data['user']['location'] is not None:
			for element in continentsandcities:
				if element[0].encode('utf-8').lower() in data['user']['location'].encode('utf-8').lower():
					if len(element[0].encode('utf-8')) > len_continent:
						len_continent = len(element[0].encode('utf-8'))
						continent = element[3].encode('utf-8')[:-1]
						element_temp = element
				if element[1].encode('utf-8').lower() in data['user']['location'].encode('utf-8').lower():
					if len(element[1].encode('utf-8')) > len_continent:
						len_continent = len(element[1].encode('utf-8'))
						continent = element[3].encode('utf-8')[:-1]
						element_temp = element
				if element[2].encode('utf-8').lower() in data['user']['location'].encode('utf-8').lower() and element[2].encode('utf-8') != "":
					if len(element[2].encode('utf-8')) > len_continent:
						len_continent = len(element[2].encode('utf-8'))
						continent = element[3].encode('utf-8')[:-1]
						element_temp = element
			if continent != "":
				if "raspberry" in data['text'].encode('utf-8').lower():
					choice = "R"
				else:
					choice = "A"
				tweetstring = data['text'].encode('utf-8')
				tweetfrom =  "Tweet from: "+data['user']['location'].encode('utf-8')
				print ("Tweet about: "+choice)
				print ("Selected Db element: "+element_temp[0]+","+element_temp[1]+","+element_temp[2]+","+element_temp[3][:-1])
				print (tweetfrom)
				print ("Continent: "+continent)
				print (tweetstring+"\n")
				found = True
			else:
				lost_cities = open("lost_cities","a")
				lost_cities.write(data['user']['location'].encode('utf-8')+"\n")
				lost_cities.close()
		return True

    def on_error(self, status):
		#print (status)
		return False


        

#def show_info():
	#ev = pygame.event.poll()
#	while ev.type!=pygame.QUIT:
#		found = True
#		ev = pygame.event.poll()
#		textfrom = pyfont.render(tweetfrom,True,(200,200,200))
#		textstring = pyfont.render(tweetstring,True,(200,200,200))
		#print (tweetstring)
#		windowSurface.fill((0,0,0))
#		windowSurface.blit(textfrom,(10,60))
#		windowSurface.blit(textstring,(10,100))
#		pygame.display.flip()
		#for x in range(255):
		#	windowSurface.fill((0,0,0))
		#	label.set_alpha(255-x)
		#	windowSurface.blit(label,(200,100))
		#	pygame.display.flip()
			#pygame.time.delay(20)
#	pygame.quit()
#	sys.exit()

def show_npxl():
	global found
	global choice
	# LED strip configuration:
	LED_COUNT      = 26      # Number of LED pixels.
	LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
	#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
	LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
	LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
	LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
	LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
	LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
	LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
    	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	#color_continent=Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
	print ('Press Ctrl-C to quit.')
	while True:
		#color_continent=Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
		if choice == "R":
			color_continent=Color(230,50,200)
		else:
			color_continent=Color(50,50,250)
		if "Europe" in continent:
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, Color(0,0,0))
			for i in range(9,12):
				strip.setPixelColor(i,color_continent)
			strip.setPixelColor(25,color_continent)
			strip.show()
			found = False
			#print ("EUROPE")
		if "Asia" in continent:
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, Color(0,0,0))
			for i in range(12,17):
				strip.setPixelColor(i,color_continent)
			strip.show()
			found = False
			#print ("ASIA")
		if "Africa" in continent:
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, Color(0,0,0))
			for i in range(22,26):
				strip.setPixelColor(i,color_continent)
			strip.show()
			found = False
			#print ("AFRICA")
		if "Australia" in continent:
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, Color(0,0,0))
			for i in range(17,22):
				strip.setPixelColor(i,color_continent)
			strip.show()
			found = False
			#print ("AUSTRALIA")
		if "North America" in continent:
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, Color(0,0,0))
			for i in range(4,9):
				strip.setPixelColor(i,color_continent)
			strip.show()
			found = False
			#print ("NORTHAMERICA")
		if  "South America" in continent:
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, Color(0,0,0))
			for i in range(0,4):
				strip.setPixelColor(i,color_continent)
			strip.show()
			found = False
		time.sleep(2)


if __name__ == '__main__':
#    s = threading.Thread(target=show_info)
#    s.start()
	npxl = threading.Thread(target=show_npxl)
	npxl.start()
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	stream = Stream(auth, l)
	stream.filter(track=search_strings)

