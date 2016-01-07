import RPi.GPIO as GPIO
import time
import pygame


GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN,GPIO.IN)
time.sleep(2)
playing = 0
start = 0
count = 0
limit = 10
while True:
	time.sleep(1)
	if GPIO.input(PIR_PIN):
		if playing == 0:
			start = 1
		if playing == 1:
			start = 0
		count = 0
		#print "PIR activat"
		if start == 1:
			pygame.mixer.init()
			pygame.mixer.music.load("/home/pi/eb.mp3")
			pygame.mixer.music.play(-1,0.0)
			playing = 1
			#print "MUSICA inici"
	if count == limit and playing == 1:
		playing = 0
		pygame.mixer.music.stop()
		pygame.mixer.quit()
		#print "MUSICA stop"
	if count == limit:
		count = 0
	#print "temps: "+str(count)
	count = count + 1
		
	
