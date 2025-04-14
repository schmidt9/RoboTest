# https://github.com/SyedUmaidAhmed/Record-and-listen-your-voice-using-Python-Raspberry-Pi/blob/master/Recordlisten.py

import subprocess
from time import sleep

proc = subprocess.Popen(['arecord --device=hw:2,0 --duration=10 --format S16_LE --rate 44100 -V mono -c1 test.wav'], shell=True)
print("Starting record...")
sleep(10)
proc.terminate()
print("\nRecording done, going to play")

broc = subprocess.Popen(['aplay --device=plughw:0,0 test.wav'], shell=True)