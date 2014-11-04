import picamera
import Image

savefile="/home/pi/capt.jpg"
savefile_t="/home/pi/capt_t.jpg"
size= 200,200
camera=picamera.PiCamera()
camera.start_preview()
i=raw_input()
camera.capture(savefile)
camera.stop_preview()
im=Image.open(savefile)
im.thumbnail(size,Image.ANTIALIAS)
im.save(savefile_t,"JPEG")

