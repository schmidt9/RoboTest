import logging
import datetime

# from https://stackoverflow.com/a/13733863/3004003

_logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
_logger.addHandler(handler)
_logger.setLevel(logging.DEBUG)

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

    _logger.debug(message)


def start_measure():
    log("Time measure started")
    global measure_time
    measure_time = True


def stop_measure():
    global measure_time
    measure_time = False
    log("Time measure stopped")


if __name__ == "__main__":
    start_measure()
    log("test log message")
    stop_measure()
