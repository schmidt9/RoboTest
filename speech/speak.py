import os
import threading
import time
import requests
import player
from pathlib import Path
import microphone_utils
import logger
from piper.piper_server import http_server


root_path = Path(__file__).parent


def start_server():
    model_path = f"{root_path}/piper/model/ru_RU-dmitri-medium.onnx"
    http_server.main(["--model", model_path])


def speak(text: str):
    logger.start_measure()

    microphone_utils.toggle_microphone(False)

    speak_text(text)

    microphone_utils.toggle_microphone(True)

    logger.stop_measure()


def speak_text(text: str):
    logger.log(f"Start speaking text '{text}'")

    piper_url = "http://localhost:5000"
    output_file_path = f"{root_path}/output.wav"
    payload = {"text": text}

    connection_tries = 60

    for i in range(connection_tries):
        try:
            request = requests.get(piper_url, params=payload, timeout=60)
            status = request.status_code

            if status == 200:
                with open(output_file_path, "wb") as fd:
                    for chunk in request.iter_content(128):
                        fd.write(chunk)

                player.play_file(output_file_path)

                os.remove(output_file_path)

                logger.log("End speaking text")

                break
            else:
                logger.log(f"Enexpected status code {status}")
                time.sleep(1)
        except requests.exceptions.ConnectionError as ex:
            logger.log(f"{ex} Trying to connect to piper server (try {i + 1})")
            time.sleep(1)
            pass


if __name__ == "__main__":
    thread = threading.Thread(target=start_server, name="Piper server")
    thread.daemon = True
    thread.start()

    for i in range(3):
        speak(f"Привет, это тестовый текст {i}")
        logger.log("===============================")
