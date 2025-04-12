import torch
import sounddevice as sd
import time
from pathlib import Path

root_path = Path(__file__).parent
local_file_ru = f'{root_path}/silero/v4_ru.pt'
sample_rate = 48000  # 8000, 24000, 48000 - частота дискретизации генерируемого аудиопотока
speaker = 'kseniya'  # aidar, baya, kseniya, xenia, random - модель голоса
put_accent = True
put_yo = False
device = torch.device('cpu')  # cpu или gpu
torch.set_num_threads(8)  # количество задействованных потоков CPU

model = torch.package.PackageImporter(
    local_file_ru).load_pickle("tts_models", "model")

torch._C._jit_set_profiling_mode(False)
torch.set_grad_enabled(False)
model.to(device)
sd.default.device = 0  # аудиоустройство для вывода

def speak(text: str):
    print(f"Starting text-to-speech for text'{text}'")

    audio = model.apply_tts(text=text + "..",
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    print(f"Got audio with length {len(audio)}")

    sd.play(audio, sample_rate)
    time.sleep((len(audio) / (sample_rate)) + 0.5)
    sd.stop()

    del audio  # освобождаем память


if __name__ == "__main__":
    speak("Привет, это тестовый текст")
