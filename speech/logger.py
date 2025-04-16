import logging

# from https://stackoverflow.com/a/13733863/3004003

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def log(message: str):
    logger.debug(message)

if __name__ == "__main__":
    log("test log message")