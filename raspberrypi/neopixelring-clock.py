# Nepixel 24 led ring clock by ferri.fc at gmail.com
# Instructions:
# sudo apt-get update
# sudo apt-get install build-essential python-dev git scons swig
# git clone https://github.com/jgarff/rpi_ws281x.git
# cd rpi_ws281x
# scons
# cd python
# sudo python setup.py install
import time

from neopixel import *


# LED strip configuration:
LED_COUNT      = 24      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	hourcolor=Color(250,50,50)
	minutecolor=Color(50,250,50)
	secondcolor=Color(50,50,250)
	black=Color(0,0,0)
	print ('Press Ctrl-C to quit.')
	norepeat=0
	while True:
		hour=int(time.strftime("%H"))
		minute=int(round(float(time.strftime("%M"))*24.0/60.0))
		second=int(round(float(time.strftime("%S"))*24.0/60.0))
		if hour==24:
			hour=0
		if minute==24:
			minute=0
		if second==24:
			second=0
		if second==1:
			norepeat=0
		if second==0 and norepeat==0:
			for i in range(24):
				strip.setPixelColor(i, black)
				strip.show()
				time.sleep(50/1000.0)
			strip.setPixelColor(second, secondcolor)
			strip.show()
			norepeat=1

		else:
			strip.setPixelColor(second, secondcolor)
			strip.setPixelColor(minute, minutecolor)
			strip.setPixelColor(hour, hourcolor)
			strip.show()
