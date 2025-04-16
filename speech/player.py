import os
import subprocess


def play_file(file_path: str):
    print("Start playing file")

    subprocess.run([f"aplay --device=plughw:0,0 {file_path}"], shell=True)

    print("End playing file")


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = f"{dir_path}/sound/mixkit-correct-answer-tone-2870.wav"
    play_file(file_path)
