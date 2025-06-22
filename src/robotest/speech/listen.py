import sounddevice as sd
import vosk
import json
import queue
from pathlib import Path
import commands
import microphone_utils
import notifications
import speak
import logger

root_path = Path(__file__).parent
model_path = f"{root_path}/vosk/vosk-model-small-ru-0.22"
model = vosk.Model(model_path)  # Модель нейросети
samplerate = 44100  # Частота дискретизации микрофона
q = queue.Queue()  # Потоковый контейнер


def q_callback(indata, frames, time, status):
    q.put(bytes(indata))


def voice_listen():
    speak.start_server()

    speak.speak(f"Запуск завершен, можете обращаться ко мне как... {commands.name_alias[0]}")

    logger.log("Start listening to voice")
    
    should_recognize_command = False

    with sd.RawInputStream(
        callback=q_callback,
        channels=1,
        samplerate=samplerate,
        device=microphone_utils.microphone_device_id,
        dtype="int16",
    ):
        recognizer = vosk.KaldiRecognizer(model, samplerate)

        sd.sleep(-20)

        while True:
            data = q.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())["text"]

                if result:
                    logger.log(f"Фраза целиком: {result}")

                    if commands.recognize_name(result):
                        should_recognize_command = True
                        notifications.play_ready_notification()
                        speak.speak("Я слушаю")
                    else:
                        if should_recognize_command:
                            speak.speak(f"Выполняю команду... {result}")

                            is_command_recognized = commands.recognize_command(result)

                            if is_command_recognized:
                                should_recognize_command = False
                                speak.speak("Команда выполнена, жду следующую")
                            else:
                                speak.speak("Не понял команду, повторите еще раз")
            else:
                result = json.loads(recognizer.PartialResult())["partial"]
                if result:
                    logger.log(f"Поток: {result}")


if __name__ == "__main__":
    voice_listen()
