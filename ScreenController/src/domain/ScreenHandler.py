import logging
from io import BytesIO
from .FragmentScreenTaker import FragmentScreenTaker
from .HealthBar import HealthBar


class ScreenHandler:
    def __init__(self):
        """
        Initialize the ScreenHandler with a FragmentScreenTaker instance.
        :param fragment_screentaker: Instance of FragmentScreenTaker used for taking screenshots.
        """
        self.fragment_screentaker = FragmentScreenTaker()
        self.health_bar = HealthBar()

    def aggregate_screen_data(self):
        take_in_memory_image_buffer = self.fragment_screentaker.take_screenshot_in_memory()

        health_bar_res = self.health_bar.calculate_red_bar_percentage(take_in_memory_image_buffer)

        return {
            "health_bar": health_bar_res
        }