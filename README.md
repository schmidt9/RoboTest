# RoboTest

Orange Pi 3B vision and speech recognition

# TTS setup

https://habr.com/ru/companies/timeweb/articles/772080/ - hardware setup
https://habr.com/ru/companies/timeweb/articles/817929/ - software setup

pip install sounddevice

# Piper

Piper is faster then Silero

https://github.com/rhasspy/piper/tree/master?tab=readme-ov-file#usage

echo "Привет мир" | piper --model ru_RU-dmitri-medium.onnx --output_file test.wav 

echo "Привет мир 16 50" | piper --model ru_RU-dmitri-medium.onnx --output-raw | aplay --device=plughw:0,0 -r 22050 -f S16_LE -t raw -

# helpers

- list record devices
arecord -l

- list playback devices
aplay -l


