import os
import sounddevice
import soundfile

def play_name_notification():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = f'{dir_path}/sound/mixkit-correct-answer-tone-2870.wav'  # Извлечение данных и частоты дискретизации из файла
    data, samplerate = soundfile.read(file_path, dtype='float32')
    sounddevice.play(data, samplerate)
    sounddevice.wait()

if __name__ == "__main__":
    play_name_notification()
