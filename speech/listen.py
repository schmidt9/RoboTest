import os
import sounddevice as sd
import vosk
import json
import queue
from pathlib import Path
import commands
import microphone_utils

root_path = Path(__file__).parent
model_path=f"{root_path}/vosk/vosk-model-small-ru-0.22"
model = vosk.Model(model_path)                                  # Модель нейросети
samplerate = 44100                                              # Частота дискретизации микрофона
q = queue.Queue()                                               # Потоковый контейнер


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
                    commands.recognize_command(res)
                    break
            else:
                res = json.loads(rec.PartialResult())["partial"]
                if res:
                    print(f"Поток: {res}")


if __name__ == "__main__":
    voice_listen()