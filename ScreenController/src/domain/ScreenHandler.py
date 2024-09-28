import logging

from ..utils.FragmentScreenTaker import FragmentScreenTaker
from ..utils.HealthBar import HealthBar
from ..utils.RadarStatus import RadarStatus
from ..utils.TargetName import TargetName
from ..consts import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)


class ScreenHandler:
    def __init__(self):
        """
        Initialize the ScreenHandler with a FragmentScreenTaker instance.
        :param fragment screen-taker: Instance of FragmentScreenTaker used for taking screenshots.
        """
        self.fst = FragmentScreenTaker()
        self.health_bar = HealthBar()
        self.radar_status = RadarStatus()
        self.target_name = TargetName()

    def aggregate_screen_data(self):

        health_cords = {
            'L': 800,
            'T': 53,
            'W': 360,
            'H': 7
        }
        health_bar_buffer = self.fst.take_screenshot_in_memory(health_cords)
        health_bar_res = self.health_bar.calculate_red_bar_percentage(health_bar_buffer)

        radar_cords = {
            'L': 995,
            'T': 170,
            'W': 90,
            'H': 90
        }
        radar_status_buffer = self.fst.take_screenshot_in_memory(radar_cords)

        radar_status_image = self.radar_status.load_image(radar_status_buffer)

        target_dots = self.radar_status.count_red_dots(radar_status_image)
        logger.debug(f"target_dots {target_dots}")

        direction = self.radar_status.determine_direction_based_on_rectangle(radar_status_image)
        logger.debug(f"direction {direction}")

        target_name_cords = {
            'L': 420,
            'T': 70,
            'W': 360,
            'H': 40
        }

        target_name_buffer = self.fst.take_screenshot_in_memory(target_name_cords)

        target_name_res = self.target_name.extract_text_from_image(target_name_buffer)
        logger.debug(f"target_name_res {target_name_res}")

        return {
            "health_bar": health_bar_res,
            "target_name": target_name_res,
            "target_dots": target_dots,
            "direction": direction
        }