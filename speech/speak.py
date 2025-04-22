import os
import subprocess
from pathlib import Path
import microphone_utils
import logger
import asyncio


root_path = Path(__file__).parent

llm_tts_process = None


def start_server():
    piper_path = f"{root_path}/piper/piper_server_binary/piper"
    piper_model_path = f"{root_path}/piper/model/ru_RU-dmitri-medium.onnx"

    # using modified Piper version
    # https://github.com/rhasspy/piper/pull/378
    # https://github.com/createcandle/voco/blob/f806a5d19ee30ddb764d8b87d0215df4f39f3645/pkg/voco_adapter.py#L12317

    tts_command = [
        piper_path,
        "--model",
        piper_model_path,
        "--server",
        "--json-input",
        "--output-raw",
        "|",
        "aplay"
    ]

    tts_command_part2 = [
        "--device=plughw:0,0",
        "-r",
        "22050",
        "-f",
        "S16_LE",
        "-t",
        "raw",
        "-"
    ]

    tts_command += tts_command_part2

    tts_command_str = " ".join(tts_command)

    logger.log(f"Starting Piper with command:\n{tts_command_str}")

    my_env = os.environ.copy()

    global llm_tts_process
    llm_tts_process = subprocess.Popen(
        args=tts_command_str,
        env=my_env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        text=True,
        bufsize=1,
        shell=True,
    )

    os.set_blocking(llm_tts_process.stdout.fileno(), False)

    if llm_tts_process.poll() is None:
        logger.log("Piper process started successfully")
    else:
        logger.log("Error, Piper process failed to start")


def speak(text: str):
    microphone_utils.toggle_microphone(False)

    speak_text(text)

    microphone_utils.toggle_microphone(True)


def speak_text(text: str):
    poll_code = llm_tts_process.poll()

    if poll_code is not None:
        logger.log(f"Piper process terminated with code {poll_code}")
        return

    logger.log(f"Scheduled text for TTS '{text}'")

    json_text = '{"text": "' + text.replace('"', '\\"') + '"}\n'

    llm_tts_process.stdin.write(json_text)
    llm_tts_process.stdin.flush()  # TODO: wait for audio finish


if __name__ == "__main__":
    start_server()

    for i in range(3):
        speak(f"Привет, это тестовый текст {i}")
        logger.log("===============================")

    loop = asyncio.get_event_loop()

    try:
        loop.run_forever()
    finally:
        loop.close()
