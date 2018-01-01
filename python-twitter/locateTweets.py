#!/usr/bin/python

from __future__ import absolute_import, print_function

import os
from subprocess import call
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import scrollphat
import threading
import time


script_path = os.path.dirname(os.path.realpath(__file__))

scrollphat.set_brightness(2)


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

search_strings = ['arduino']

class StdOutListener(StreamListener):
    """
    A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        data  = json.loads(data)
        if data['user']['location'] is not None:
			scrollphat.clear()
			scrollphat.write_string(search_strings[0].upper() + " # " + data['user']['location'].encode('utf-8').upper(), 11)
			#print ("USER:",data['user']['name'].encode('utf-8'),"@",data['user']['screen_name'].encode('utf-8'))
			print ("LOCATION DATA:")
			print (data['user']['location'])
			#print ("TEXT:",data['text'].encode('utf-8'))
        return True

    def on_error(self, status):
        #print (status)
        scrollphat.clear()
        return False

def scroll_text():
    scrollphat.set_brightness(2)
    while True:
         try:
             scrollphat.scroll()
             time.sleep(0.1)
         except KeyboardInterrupt:
             scrollphat.clear()
             sys.exit(-1)
             


if __name__ == '__main__':
    s = threading.Thread(target=scroll_text)
    s.start()
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=search_strings)

