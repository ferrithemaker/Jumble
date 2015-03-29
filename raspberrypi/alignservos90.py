#!/usr/bin/env python
 
import time
from pyfirmata import Arduino, util, SERVO

#board=Arduino("/dev/ttyACM0")
#board=Arduino("/dev/ttyUSB0")
board=Arduino("/dev/ttyAMA0")
board.digital[9].mode = SERVO # humidity
board.digital[8].mode = SERVO # temp
board.digital[11].mode = SERVO # light
while True:
	board.digital[9].write(90)
	board.digital[8].write(90)
	board.digital[11].write(90)
	time.sleep(1)
