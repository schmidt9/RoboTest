import os
import player

def play_name_notification():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = f'{dir_path}/sound/mixkit-correct-answer-tone-2870.wav'  # Извлечение данных и частоты дискретизации из файла
    player.play_file(file_path)

if __name__ == "__main__":
    play_name_notification()
