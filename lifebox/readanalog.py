import pyfirmata
 
# Definition of the analog pin
PINS = (0, 1, 2, 3, 4)
 
# Creates a new board 
board = pyfirmata.Arduino("/dev/ttyACM0")
#print "Setting up the connection to the board ..."
it = pyfirmata.util.Iterator(board)
it.start()
 
# Start reporting for defined pins
for pin in PINS:
    board.analog[pin].enable_reporting()
while(True):
	board.pass_time(2)
	f = open('controllerdata','w')
	for pin in PINS:
                #print "Analog Pin %i : %s" % (pin, board.analog[pin].read())
			f.write(str(board.analog[pin].read()))
			f.write('\n')
	f.close()
 
# Loop for reading the input. Duration approx. 10 s
#for i in range(1, 11):
#	print "\nValues after %i second(s)" % i
#	for pin in PINS:
#		print "Analog Pin %i : %s" % (pin, board.analog[pin].read())
#	board.pass_time(1)	

board.exit()
