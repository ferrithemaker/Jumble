import time
from twython import TwythonStreamer
import subprocess

def say(words):
	devnull = open("/dev/null","w")
	subprocess.call(["espeak","-v", "en-rp",words],stderr=devnull)

# Search terms
TERMS = '@DIYProjectLog'


# Twitter application authentication
APP_KEY = 'wUQEDIMF5kGHJE8CucdwzKGRt'
APP_SECRET = 'YXiKfBySvI8N06GY5lr2zsIwPHfqj8d9n0nQuGVmKs8hrgyP9T'
OAUTH_TOKEN = '2609358157-22C6X9IqHZpPpZckA4HXTIu9v97QqalIg2PZWha'
OAUTH_TOKEN_SECRET = 'bDR9BJ7ebMaqLBxppt9Xy7IoTz6yk3Y4c6r0EHlh8si76'

# Setup callbacks from Twython Streamer
class TalkingTwitter(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        print data['text'].encode('utf-8')
                        print
			#say(data['text'].encode('utf-8'))
			say("You have been mentioned in Twitter")



# Create streamer
try:
	stream = TalkingTwitter(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
	print "Bye Bye!"
