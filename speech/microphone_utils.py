import os

microphone_device_id = 2                                       # Индекс аудиоустройства (микрофон)

def toggle_microphone(on: bool):
    on_mic  = f'amixer -c {microphone_device_id} set Mic cap'  # команда отключения глушилки
    off_mic = f'amixer -c {microphone_device_id} set Mic nocap'# команда на глушение микрофона

    if on:
        print("Enabling microphone")
        os.system(on_mic)
    else:
        print("Disabling microphone")
        os.system(off_mic)