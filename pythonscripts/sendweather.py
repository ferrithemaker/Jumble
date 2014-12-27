# Lottery Wall by Ferran Fabregas ferri.fc@gmail.com
import random, math
import Image, sys
import time
from twython import Twython
from twython import TwythonStreamer

import Adafruit_DHT

import subprocess

# Setup callbacks from Twython Streamer
class TwitterController(TwythonStreamer):
        def on_success(self, data):
		#print data
                if 'text' in data:
                        twitterString=data['text'].encode('utf-8')
			stringParts=twitterString.split(' ')                        
			print twitterString
			if len(stringParts)==2 and stringParts[1]=="weather": 
				humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
				wdata="@"+data['user']['screen_name'].encode('utf-8')+" "+'My home temperature={0:0.1f}*C - Home humidity={1:0.1f}%'.format(temperature, humidity)+" History graph: http://www.ferranfabregas.info/weatherstation/showdata.html"
				twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
				twitter.update_status(status=wdata)
				#print wdata

# Your twitter ID
TERMS = '@DIYProjectLog'


# Twitter application authentication
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

print "LISTENING TWITTER....."
# Create streamer
#twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
#twitter.update_status(status="First Tweet from Python! :D -test-")

try:
	stream = TwitterController(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
	print "Bye Bye! :)"
