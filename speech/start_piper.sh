!#/bin/bash

# https://github.com/rhasspy/piper/issues/376#issuecomment-2745926719

echo "feed text to it from other processes to be read out without delay:"
echo "echo \"hello\" > /tmp/piper-fifo"

# create named pipe and keep it open:
rm -f /tmp/piper-fifo && mkfifo /tmp/piper-fifo && tail -f /dev/null > /tmp/piper-fifo &

# start piper, which will keep running indefinitely:
/home/orangepi/Documents/dev/RoboTest/speech/piper/piper --model /home/orangepi/Documents/dev/RoboTest/speech/piper/model/ru_RU-dmitri-medium.onnx --output-raw  < /tmp/piper-fifo | aplay --device=plughw:0,0 -r 22050 -f S16_LE -t raw -
