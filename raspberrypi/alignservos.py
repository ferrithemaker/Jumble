#!/usr/bin/env python
 
import time
from pyfirmata import Arduino, util, SERVO

#board=Arduino("/dev/ttyACM0")
#board=Arduino("/dev/ttyUSB0")
board=Arduino("/dev/ttyAMA0")
board.digital[8].mode = SERVO # temp
board.digital[9].mode = SERVO # humidiy ok
board.digital[11].mode = SERVO # light ok
i=20
while True:
	board.digital[8].write(i)
	board.digital[9].write(i)
	board.digital[11].write(i)
	i=i+10
	if i>150:
		i=20
	time.sleep(1)
