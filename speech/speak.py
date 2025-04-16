import os
import torch
from pathlib import Path
import microphone_utils
import player
import logger

root_path = Path(__file__).parent
local_file_ru = f"{root_path}/silero/v4_ru.pt"
sample_rate = (
    24000  # 8000, 24000, 48000 - частота дискретизации генерируемого аудиопотока
)
speaker = "kseniya"  # aidar, baya, kseniya, xenia, random - модель голоса
put_accent = True
put_yo = False
device = torch.device("cpu")  # cpu или gpu
torch.set_num_threads(4)  # количество задействованных потоков CPU

model = torch.package.PackageImporter(local_file_ru).load_pickle("tts_models", "model")

torch._C._jit_set_profiling_mode(False)
torch.set_grad_enabled(False)
model.to(device)


def speak(text: str):
    logger.start_measure()
    logger.log(f"Starting TTS for text '{text}'")

    tmp_audio_path = f"{root_path}/tmp.wav"

    # https://github.com/snakers4/silero-models/discussions/262
    # save intermediate file, play it and delete
    model.save_wav(
        text=text + "..",
        speaker=speaker,
        sample_rate=sample_rate,
        put_accent=put_accent,
        put_yo=put_yo,
        audio_path=tmp_audio_path,
    )

    microphone_utils.toggle_microphone(False)

    player.play_file(tmp_audio_path)
    os.remove(tmp_audio_path)

    microphone_utils.toggle_microphone(True)

    logger.log("Finished playing")
    logger.stop_measure()


if __name__ == "__main__":
    speak("Привет, это тестовый текст")
