
import time
import telepot
from picamera import PiCamera
import RPi.GPIO as GPIO

camera = PiCamera()
camera.rotation = 180

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)
intruder = False
enabled = False

def handle(msg):
    global enabled
    global intruder
    
    command = msg['text']
    from_id = msg['from']['id']
    #chat_id = msg['chat']['id']
    #print 'Got command: %s' % command
    if from_id == 192114914:
    	if command.lower() == 'show':
        	camera.start_preview()
        	time.sleep(5)
        	camera.capture('/home/pi/image.jpg')
        	camera.stop_preview()
        	inf = open('/home/pi/image.jpg', 'rb')
        	#bot.sendMessage(chat_id,text="Done!")
        	bot.sendPhoto(chat_id,inf)
    	if command.lower() == "enable pir":
    		enabled = True
    		bot.sendMessage(chat_id,text="PIR enabled")
    	if command.lower() == "disable pir":
    		enabled = False
    		bot.sendMessage(chat_id,text="PIR disabled")
    else:
    	bot.sendMessage(from_id,text="I'm not allowed to talk with you, sorry")
    	bot.sendMessage(chat_id,text="Somebody is trying to use the chatbot")

chat_id = xxxxxxx
bot = telepot.Bot('xxxxxxxxx')
bot.message_loop(handle)
#print 'I am listening...'

while 1:
    pirvalue = GPIO.input(11)
    if pirvalue == 1 and intruder == False and enabled == True:
        intruder = True
        camera.start_preview()
        time.sleep(5)
        camera.capture('/home/pi/image.jpg')
        camera.stop_preview()
        inf = open('/home/pi/image.jpg')
        bot.sendPhoto(chat_id,inf)
    if pirvalue == 0:
    		intruder = False
    time.sleep(1)
