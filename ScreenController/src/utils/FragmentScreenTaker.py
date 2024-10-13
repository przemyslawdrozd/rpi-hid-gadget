import time
import logging
import pyautogui
from io import BytesIO
import argparse
from ..consts import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class FragmentScreenTaker:

    def __init__(self, args: argparse.Namespace):
        self.args = args

    def take_screenshot_in_memory(self, key: str, cords: dir) -> BytesIO:
        """
        Takes a screenshot of a specified region and returns it as an in-memory BytesIO object.

        Returns:
            BytesIO: The screenshot saved in an in-memory BytesIO object.
        """
        logging.info("Starting screenshot process...")

        # Measure the start time
        start_time = time.time()

        left = cords['L']
        top = cords['T']
        width = cords['W']
        height = cords['H']

        # Take a screenshot of the specified region (but do not save it)
        screenshot = pyautogui.screenshot(region=(left, top, width, height))

        # Save screenshot
        if self.args.screen:
            screenshot.save(f"{key}.png")

        # Measure the time after taking the screenshot
        screenshot_time = time.time()
        logging.info(f"Screenshot taken in {screenshot_time - start_time:.4f} seconds.")

        # Convert the screenshot to an in-memory object (BytesIO)
        img_byte_arr = BytesIO()
        screenshot.save(img_byte_arr, format="PNG")

        # Return the in-memory object
        return img_byte_arr
