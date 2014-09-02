# Script By Ferran Fabregas (ferri.fc@gmail.com)
import Image, sys, math
sys.path.append("./mcpi/api/python/mcpi")
import minecraft
import time
from twython import TwythonStreamer
import subprocess


# Init minecraft world

mc=minecraft.Minecraft.create()
mc.postToChat("Welcome to Minecraft Social Grafitti Wall")

# Get original player position

originalPlayerPosition=mc.player.getTilePos()

# Clean terrain and draw the wall

for x in range (originalPlayerPosition.x-10,originalPlayerPosition.x+10):
    for y in range (originalPlayerPosition.y,originalPlayerPosition.y+15):
	for z in range (originalPlayerPosition.z-10,originalPlayerPosition.z+10):
        	mc.setBlock(x,y,z,0)

for x in range (originalPlayerPosition.x-10,originalPlayerPosition.x+10):
    for y in range (originalPlayerPosition.y,originalPlayerPosition.y+15):
        mc.setBlock(x,y,originalPlayerPosition.z+10,1)

mc.postToChat("Wall created!")

# Your twitter ID
TERMS = '@DIYProjectLog'


# Twitter application authentication
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

# Setup callbacks from Twython Streamer
class TwitterController(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        twitterString=data['text'].encode('utf-8')
			stringParts=twitterString.split(' ')                        
			print twitterString
			if len(stringParts)==4: # If lenght is correct
				colorName=stringParts[1]
				xPos=int(stringParts[2])
				yPos=int(stringParts[3])
				# Parse and render
				colorCode=15 # Default color
				if xPos>0 and xPos<=20 and yPos>0 and yPos<=15: # Check boundaries
					if colorName=="white":
						colorCode=0
					if colorName=="orange":
						colorCode=1
					if colorName=="magenta":
						colorCode=2
					if colorName=="lightblue":
						colorCode=3
					if colorName=="yellow":
						colorCode=4
					if colorName=="lime":
						colorCode=5
					if colorName=="pink":
						colorCode=6
					if colorName=="gray":
						colorCode=7
					if colorName=="lightgray":
						colorCode=8
					if colorName=="cyan":
						colorCode=9
					if colorName=="purple":
						colorCode=10
					if colorName=="blue":
						colorCode=11
					if colorName=="brown":
						colorCode=12
					if colorName=="green":
						colorCode=13
					if colorName=="red":
						colorCode=14
					if colorName=="black":
						colorCode=15
					mc.setBlock(originalPlayerPosition.x+10-xPos,originalPlayerPosition.y+yPos-1,originalPlayerPosition.z+10,35,colorCode)
					mc.postToChat(stringParts[0]+" draw something on the wall!")


# Create streamer
try:
	stream = TwitterController(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
	print "Bye Bye! :)"



