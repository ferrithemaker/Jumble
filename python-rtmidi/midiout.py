import time
import rtmidi
import random

def chordGenerator():
    startValue = random.randint(50,60)
    return ([startValue,startValue+4,startValue+7])

def stopAllSounds():
    for i in range(50,60):
        midiout.send_message([0x80,i,30])
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print (available_ports)
print (midiout.get_port_count())
midiout.open_port(1)
stopAllSounds()

try:
    while True:
        chord = chordGenerator()
        midiout.send_message([0x90,chord[0],30])
        midiout.send_message([0x90,chord[1],30])
        midiout.send_message([0x90,chord[2],30])
        time.sleep(float(random.randint(3000,5000)/1000))
        midiout.send_message([0x80,chord[0],0])
        midiout.send_message([0x80,chord[1],0])
        midiout.send_message([0x80,chord[2],0])
except KeyboardInterrupt:
    del midiout
