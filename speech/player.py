import os
import subprocess
import pytz
import datetime
import logger
from pathlib import Path


def play_file(file_path: str):
    logger.log("Start playing file")
    
    # not using sounddevice here because it freezes on play() for some reason
    subprocess.run([f"aplay --device=plughw:0,0 {file_path}"], shell=True)

    logger.log("End playing file")


def speak_text(text: str):
    logger.log(f"Start speaking text '{text}'")

    root_path = Path(__file__).parent
    piper_path = f"{root_path}/piper"
    
    # not using sounddevice here because it freezes on play() for some reason

    command = f"echo {text} | {piper_path}/piper --model {piper_path}/model/ru_RU-dmitri-medium.onnx --output-raw | aplay --device=plughw:0,0 -r 22050 -f S16_LE -t raw -"
    logger.log(f"Executing command '{command}'")

    subprocess.run([command], shell=True)

    logger.log("End speaking text")


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = f"{dir_path}/sound/mixkit-correct-answer-tone-2870.wav"
    play_file(file_path)

    timezone = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now().astimezone(timezone)
    speak_text(f"Текущее время по Москве {now.hour} {now.minute}")
