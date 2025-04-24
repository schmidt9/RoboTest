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

echo "Привет мир 16 50" | /home/orangepi/Documents/dev/RoboTest/speech/piper/piper_server_binary/piper --model /home/orangepi/Documents/dev/RoboTest/speech/piper/model/ru_RU-dmitri-medium.onnx --output-raw | aplay --device=plughw:0,0 -r 22050 -f S16_LE -t raw -

# Piper local server

sudo apt install python3-dev
pip install piper-phonemize-cross
pip install piper-tts

python3 -m speech.piper.piper_server.http_server --model speech/piper/model/ru_RU-dmitri-medium.onnx

curl -G --data-urlencode 'text=Привет мир 16 50' -o test.wav 'localhost:5000'

# Piper binary as long-running process

https://github.com/rhasspy/piper/pull/378
https://github.com/rhasspy/piper/issues/376

# helpers

- list record devices
arecord -l

- list playback devices
aplay -l


