import os
import logger

microphone_device_id = 2                                       # Индекс аудиоустройства (микрофон)

def toggle_microphone(on: bool):
    on_mic  = f'amixer -c {microphone_device_id} set Mic cap > /dev/null'  # команда отключения глушилки
    off_mic = f'amixer -c {microphone_device_id} set Mic nocap > /dev/null'# команда на глушение микрофона

    if on:
        logger.log("Enabling microphone")
        os.system(on_mic)
    else:
        logger.log("Disabling microphone")
        os.system(off_mic)