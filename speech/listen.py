import sounddevice as sd
import vosk
import json
import queue
from pathlib import Path
import commands
import microphone_utils
import notifications

root_path = Path(__file__).parent
model_path=f"{root_path}/vosk/vosk-model-small-ru-0.22"
model = vosk.Model(model_path)                                  # Модель нейросети
samplerate = 44100                                              # Частота дискретизации микрофона
q = queue.Queue()                                               # Потоковый контейнер

should_recognize_command = False


def q_callback(indata, frames, time, status):
    q.put(bytes(indata))


def voice_listen():
    print("Start listening to voice")

    with sd.RawInputStream(callback=q_callback, 
                           channels=1, 
                           samplerate=samplerate, 
                           device=microphone_utils.microphone_device_id, 
                           dtype='int16'):
        rec = vosk.KaldiRecognizer(model, samplerate)

        sd.sleep(-20)

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())["text"]
                if res:
                    print(f"Фраза целиком: {res}")

                    global should_recognize_command

                    if commands.recognize_name(res):
                        should_recognize_command = True
                        notifications.play_name_notification()
                    else:
                        if should_recognize_command:
                            is_command_recognized = commands.recognize_command(res)

                            if is_command_recognized:
                                should_recognize_command = False
            else:
                res = json.loads(rec.PartialResult())["partial"]
                if res:
                    print(f"Поток: {res}")


if __name__ == "__main__":
    voice_listen()