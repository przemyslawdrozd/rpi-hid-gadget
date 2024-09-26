import sys
import time
import logging

from src.SCService import SCService
from src.consts import LOGGER_NAME, LOG_FORMATTING

logger = logging.getLogger(LOGGER_NAME)


def set_logger():
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(LOG_FORMATTING)
    formatter.converter = time.gmtime
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.parent = False


def main():
    logger.info("Init service")
    service = SCService()

    logger.info("Start screen controller service")
    service.start_sc_service()

    logger.info("Stop service")


if __name__ == "__main__":
    main()
