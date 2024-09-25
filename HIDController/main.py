import os
import sys
import asyncio
import logging

"""To fix ModuleNotFoundError from src files"""
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.HIDController import HIDController
from src.consts import WS_PREFIX

if __name__ == "__main__":
    logging.info("Start script")

    args = sys.argv[1:]
    ws_url_suffix = args[0]
    ws_url = f"{WS_PREFIX}.{ws_url_suffix}"

    hid_controller = HIDController(ws_url)

    # Start the event loop
    asyncio.get_event_loop().run_until_complete(hid_controller.start())
    logging.info("Close script")
