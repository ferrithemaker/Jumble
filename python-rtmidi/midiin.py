import time
import rtmidi

midiin = rtmidi.MidiIn()
available_ports = midiin.get_ports()
print available_ports
midiin.open_port(1)
while True:
	m = midiin.get_message()
	if m:
		print(m)
