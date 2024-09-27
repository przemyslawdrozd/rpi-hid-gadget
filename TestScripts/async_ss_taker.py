import asyncio
import logging
import time
import pyautogui
from io import BytesIO
from PIL import Image
import cv2
import numpy as np

BAR_PREFIX = 37

class HealthBar:
    def __init__(self):
        # Initialize HSV range for detecting red color
        self.lower_red = np.array([0, 120, 70])
        self.upper_red = np.array([10, 255, 255])

    def calculate_red_bar_percentage(self, img_byte_arr: BytesIO) -> int:
        """
        Processes an image to calculate the percentage of red in the health bar.

        Args:
            img_byte_arr: A BytesIO object containing the image.

        Returns:
            int: The approximate percentage of red in the health bar.
        """
        # Convert the in-memory image (BytesIO) to a numpy array
        img_byte_arr.seek(0)  # Ensure you're reading from the start of the BytesIO object
        pil_image = Image.open(img_byte_arr)

        # Convert the PIL image to a format OpenCV can work with (numpy array)
        image = np.array(pil_image)

        # Convert RGB (PIL format) to BGR (OpenCV format)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create a mask for the red color using initialized HSV range
        red_mask = cv2.inRange(hsv_image, self.lower_red, self.upper_red)

        # Find the total width of the bar (both red and empty parts)
        bar_height, bar_width = red_mask.shape

        # Find the number of red pixels
        red_pixels = cv2.countNonZero(red_mask)

        # Calculate the percentage of red pixels
        approx_percentage = (red_pixels / bar_width) * BAR_PREFIX

        return int(approx_percentage)


class FragmentScreenTaker:
    def __init__(self, left=400, top=100, width=360, height=80):
        """
        Initialize the region of the screen to capture.
        Args:
            left (int): X-coordinate of the top-left corner of the region.
            top (int): Y-coordinate of the top-left corner of the region.
            width (int): Width of the region.
            height (int): Height of the region.
        """
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    async def take_screenshot_in_memory(self) -> BytesIO:
        """
        Takes a screenshot of a specified region and returns it as an in-memory BytesIO object.

        Returns:
            BytesIO: The screenshot saved in an in-memory BytesIO object.
        """
        logging.info("Starting screenshot process...")

        # Measure the start time
        start_time = time.time()

        # Define the function to capture the screenshot with the region
        def capture_screenshot():
            return pyautogui.screenshot(region=(self.left, self.top, self.width, self.height))

        # Take the screenshot in a separate thread using run_in_executor
        screenshot = await asyncio.get_event_loop().run_in_executor(None, capture_screenshot)

        # Save screenshot
        screenshot.save(f"save_{start_time}.png")

        # Measure the time after taking the screenshot
        screenshot_time = time.time()
        logging.info(f"Screenshot taken in {screenshot_time - start_time:.4f} seconds.")

        # Convert the screenshot to an in-memory object (BytesIO)
        img_byte_arr = BytesIO()
        screenshot.save(img_byte_arr, format='PNG')

        # Rewind the buffer to the beginning, so it can be read
        img_byte_arr.seek(0)

        # Return the in-memory object
        return img_byte_arr


async def main():
    fragment_screen_taker = FragmentScreenTaker()
    health_bar = HealthBar()

    # Take the screenshot asynchronously
    take_in_memory_image_buffer = await fragment_screen_taker.take_screenshot_in_memory()

    # Process the health bar percentage asynchronously
    res = health_bar.calculate_red_bar_percentage(take_in_memory_image_buffer)
    print("res", res)


if __name__ == "__main__":
    asyncio.run(main())
