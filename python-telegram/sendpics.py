
import time
import telepot
from picamera import PiCamera

camera = PiCamera()
camera.rotation = 180


def handle(msg):
    chat_id = xxxxxxx
    command = msg['text']

    print 'Got command: %s' % command

    if command == 'send picture':
        camera.start_preview()
        time.sleep(5)
        camera.capture('/home/pi/image.jpg')
        camera.stop_preview()
        inf = open('/home/pi/image.jpg', 'rb')
        #bot.sendMessage(chat_id,text="Done!")
        bot.sendPhoto(chat_id,inf)


bot = telepot.Bot('xxxxxxxxxxxxxxxxxxxxxxxxxx')
bot.message_loop(handle)
print 'I am listening...'

while 1:
    time.sleep(10)
