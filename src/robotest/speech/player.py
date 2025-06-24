import os
import subprocess
from . import logger
from pathlib import Path


def play_file(file_path: str, options: str = None):
    logger.log("Start playing file")

    command = (
            f"aplay --device=plughw:0,0 {file_path}" 
            if options is None 
            else f"aplay --device=plughw:0,0 {options} {file_path}"
            )
    
    # not using sounddevice here because it freezes on play() for some reason
    subprocess.run([command], shell=True)

    logger.log("End playing file")


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = f"{dir_path}/sound/mixkit-correct-answer-tone-2870.wav"
    play_file(file_path)
