import base64
import logging
import sys
import os

from dotenv import dotenv_values

try:
    config = dotenv_values(".env")
    LOG_LEVEL = config["LOG_LEVEL"]
except Exception:
    LOG_LEVEL = os.environ["LOG_LEVEL"]

if LOG_LEVEL == "DEBUG":
    LOG_LEVEL = logging.DEBUG
elif LOG_LEVEL == "INFO":
    LOG_LEVEL = logging.INFO

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=LOG_LEVEL
)
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.propagate = False
    logger.setLevel(LOG_LEVEL)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(LOG_LEVEL)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("logs.log")
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def info(msg: str):
    logger.info(msg)


def debug(msg):
    logger.debug(msg)


def warning(msg: str):
    logger.warning(msg)


def exception(msg):
    logger.exception(msg)


def error(msg):
    logger.error(msg)
