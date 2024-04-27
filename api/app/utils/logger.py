import base64
import logging
import sys

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.propagate = False
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("logs.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def info(msg: str):
    logger.info(msg)
    # if msg.isalnum():
    #     logger.info(msg)
    # else:
    #     logger.info(base64.b64encode(msg.encode("UTF-8")))


def debug(msg):
    logger.debug(msg)


def warning(msg: str):
    logger.warning(msg)
    # if msg.isalnum():
    #     logger.warning(msg)
    # else:
    #     logger.warning(base64.b64encode(msg.encode("UTF-8")))


def exception(msg):
    logger.exception(msg)


def error(msg):
    logger.error(msg)
