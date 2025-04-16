import logging
import datetime

# from https://stackoverflow.com/a/13733863/3004003

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

start_time: datetime.datetime = None
measure_time: bool = False

def log(message: str):
    global start_time

    if measure_time:
        if start_time is None:
            start_time = datetime.datetime.now()

        duration = datetime.datetime.now() - start_time
        message += f" [+{duration.seconds} sec]"
    else:
        start_time = None

    logger.debug(message)

if __name__ == "__main__":
    log("test log message")