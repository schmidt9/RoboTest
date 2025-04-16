import os
import subprocess

def play_name_notification():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = f'{dir_path}/sound/mixkit-correct-answer-tone-2870.wav'  # Извлечение данных и частоты дискретизации из файла

    print("Start playing notification")

    subprocess.run([f'aplay --device=plughw:0,0 {file_path}'], shell=True)

    print("End playing notification")

if __name__ == "__main__":
    play_name_notification()
