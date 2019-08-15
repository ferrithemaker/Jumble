from pyfirmata import ArduinoMega, util
 

board = ArduinoMega('/dev/ttyACM0')
it = util.Iterator(board)
it.start()
 
# Start reporting for defined pins
for pin in range (0,11):
    board.analog[pin].enable_reporting()
while(True):
	board.pass_time(2)
	f = open('controllerdata','w')
	for pin in range (0,11):
		print ("Analog Pin %i : %s" % (pin, int(board.analog[pin].read()*1023)))
		f.write(str(int(board.analog[pin].read()*1023)))
		f.write('\n')
	f.close()

board.exit()
