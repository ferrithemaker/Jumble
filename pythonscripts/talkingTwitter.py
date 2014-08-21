import time
from twython import TwythonStreamer
import subprocess

def say(words):
	devnull = open("/dev/null","w")
	subprocess.call(["espeak","-v", "en-rp",words],stderr=devnull)

# Search terms
TERMS = '@DIYProjectLog'


# Twitter application authentication
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

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
