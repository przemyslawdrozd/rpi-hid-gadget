import os
import sys
import asyncio
import logging
import time

"""To fix ModuleNotFoundError from src files"""
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.HIDController import HIDController
from src.consts import WS_PREFIX, LOGGER_NAME, LOG_FORMATTING

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


if __name__ == "__main__":
    set_logger()
    logging.info("Start script")

    args = sys.argv[1:]
    ws_url_suffix = args[0]
    ws_url = f"{WS_PREFIX}.{ws_url_suffix}"

    hid_controller = HIDController(ws_url)

    # Start the event loop
    asyncio.get_event_loop().run_until_complete(hid_controller.start())
    logging.info("Close script")
