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

        radar_targets_cords = {
            'L': 1472,
            'T': 40,
            'W': 200,
            'H': 200
        }
        radar_targets_buffer = self.fst.take_screenshot_in_memory(radar_targets_cords)
        radar_targets_image = self.radar_status.load_image(radar_targets_buffer)
        target_dots = self.radar_status.count_red_dots(radar_targets_image)
        logger.debug(f"target_dots {target_dots}")

        
        radar__direction_cords = {
            'L': 1545,
            'T': 113,
            'W': 60,
            'H': 60
        }
        radar_direction_buffer = self.fst.take_screenshot_in_memory(radar__direction_cords)
        radar_direction_image = self.radar_status.load_image(radar_direction_buffer)
        direction = self.radar_status.determine_direction_based_on_rectangle(radar_direction_image)
        logger.debug(f"direction {direction}")

        target_name_cords = {
            'L': 850,
            'T': 30,
            'W': 250,
            'H': 25
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