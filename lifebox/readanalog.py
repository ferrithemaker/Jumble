from pyfirmata import ArduinoMega, util
import subprocess

bashCommand = "fuser -k /dev/ttyACM0"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

check = True
pinArray = [512,512,512,512,512,512,512,512,512,512,512]

board = ArduinoMega('/dev/ttyACM0')
it = util.Iterator(board)
it.start()
 
# Start reporting for defined pins
for pin in range (0,11):
    board.analog[pin].enable_reporting()
while(True):
	board.pass_time(2)
	f = open('controllerdata','w')
	index = 0
	for pin in range (0,11):
		value = board.analog[pin].read()
		if value is not None:
			#f.write(str(int(value*1023)))
			pinArray[index] = int(value*1023)
			if check:
				#print ("Analog Pin %i : %s" % (pin, int(value*1023)))
				print("Readings Ok, you can start Lifebox!")
				check = False
		#board.pass_time(0.2)
		index = index + 1
	for element in pinArray:
		f.write(str(element))
		f.write('\n')
	f.close()

board.exit()
