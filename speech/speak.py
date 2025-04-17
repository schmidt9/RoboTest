import subprocess
from pathlib import Path
import microphone_utils
import logger


def speak(text: str):
    logger.start_measure()

    microphone_utils.toggle_microphone(False)

    speak_text(text)

    microphone_utils.toggle_microphone(True)

    logger.stop_measure()


def speak_text(text: str):
    logger.log(f"Start speaking text '{text}'")

    root_path = Path(__file__).parent
    piper_path = f"{root_path}/piper"

    command = f"echo {text} | {piper_path}/piper --model {piper_path}/model/ru_RU-dmitri-medium.onnx --output-raw | aplay --device=plughw:0,0 -r 22050 -f S16_LE -t raw -"
    logger.log(f"Executing command '{command}'")

    subprocess.run([command], shell=True)

    logger.log("End speaking text")


if __name__ == "__main__":
    # first speak call can take significant time, but following calls should be much faster (~x5)
    for i in range(3):
        speak(f"Привет, это тестовый текст {i}")
        logger.log("===============================")
