import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print available_ports
midiout.open_port(1)
note_on = [0x90,60,112] # channel 1, note C , velocity 112
note_off = [0x80,60,0]
midiout.send_message(note_on)
time.sleep(0.5)
midiout.send_message(note_off)
del midiout
