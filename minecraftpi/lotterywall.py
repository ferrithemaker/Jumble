# Lottery Wall by Ferran Fabregas ferri.fc@gmail.com
import random, math
import Image, sys
sys.path.append("./mcpi/api/python/mcpi")
import minecraft
import time
from twython import TwythonStreamer
import subprocess

# COLOR MAPPING

def colormap(pixel):
    white=(221,221,221)
    orange=(219,125,62)
    magenta=(179,80,188)
    lightblue=(107,138,201)
    yellow=(177,166,39)
    lime=(65,174,56)
    pink=(208,132,153)
    gray=(64,64,64)
    lightgray=(154,161,161)
    cyan=(46,110,137)
    purple=(126,61,181)
    blue=(46,56,141)
    brown=(79,50,31)
    green=(53,70,27)
    red=(150,52,48)
    black=(25,22,22)

    colors=(white,orange,magenta,lightblue,yellow,lime,pink,gray,lightgray,cyan,purple,blue,brown,green,red,black)

    thecolor=0
    finalresult=256*256*256
    for idx,color in enumerate(colors):
        result=math.fabs(color[0]-pixel[0])+math.fabs(color[1]-pixel[1])+math.fabs(color[2]-pixel[2])
        if result<finalresult:
            finalresult=result
            thecolor=idx
    return thecolor

# Setup callbacks from Twython Streamer
class TwitterController(TwythonStreamer):
        def on_success(self, data):
		#print data
                if 'text' in data:
                        twitterString=data['text'].encode('utf-8')
			stringParts=twitterString.split(' ')                        
			print twitterString
			if len(stringParts)==3 and stringParts[1].isdigit() and stringParts[2].isdigit() : # If lenght is correct and are digits
				xPos=int(stringParts[1])
				yPos=int(stringParts[2])
				# Parse and render
				if xPos>0 and xPos<=im.size[0]+1 and yPos>0 and yPos<=im.size[1]+1:
					mc.setBlock(-(im.size[0]/2)+xPos-1,29,-(im.size[1]/2)+yPos-1,0)
					if xPos==winposX and yPos==winposY:
						mc.postToChat(data['user']['screen_name'].encode('utf-8')+" You WIN!!!")
						print data['user']['screen_name'].encode('utf-8')+" You WIN!!!"
						for x in range (-(winim.size[0]/2),(winim.size[0]/2)):
    							for y in range (-(winim.size[1]/2),(winim.size[1]/2)):
        							mc.setBlock(x,29,y,35,colormap(winpixels[x+(winim.size[0]/2),y+(winim.size[1]/2)]))
						#mc.player.setTilePos(0,30,0)						
						sys.exit()
					else:
						mc.postToChat(data['user']['screen_name'].encode('utf-8')+" Try again!!!")


# LOAD IMAGE FILES
im=Image.open("./bitslogo.jpg")
pixels=im.load()
#print im.size
winim=Image.open("./youwin.jpg")
winpixels=winim.load()

# CALCULATE WINNER NUMBERS
winposX=random.randint(0,im.size[0])
winposY=random.randint(0,im.size[1])

# fixed winner position (testing)
winposX=56
winposY=43


# Your twitter ID
TERMS = '@DIYProjectLog'


# Twitter application authentication
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

# INIT MINECRAFT WORLD
mc=minecraft.Minecraft.create()
mc.postToChat("Welcome to Lottery Wall!")
for x in range (-(im.size[0]/2),(im.size[0]/2)):
    for y in range (-(im.size[1]/2),(im.size[1]/2)):
        mc.setBlock(x,29,y,35,colormap(pixels[x+(im.size[0]/2),y+(im.size[1]/2)]))
        print "Print position:(%i,%i)"%(x+(im.size[0]/2),y+(im.size[1]/2))
mc.player.setTilePos(0,30,0)
print "RENDER FINISHED!!"
print "LISTENING TWITTER....."
# Create streamer
try:
	stream = TwitterController(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
	print "Bye Bye! :)"
