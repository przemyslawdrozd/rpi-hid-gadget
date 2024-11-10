import logging
import argparse

from ..utils.FragmentScreenTaker import FragmentScreenTaker
from ..utils.HealthBar import HealthBar
from ..utils.RadarStatus import RadarStatus
from ..utils.TargetName import TargetName
from ..utils.CPBar import CPBar
from ..utils.MPBar import MPBar
from ..utils.TVReader import TVReader
from ..consts import LOGGER_NAME, CORDS

logger = logging.getLogger(LOGGER_NAME)


class ScreenHandler:
    def __init__(self, anti, args: argparse.Namespace):
        """
        Initialize the ScreenHandler with a FragmentScreenTaker instance.
        :param fragment screen-taker: Instance of FragmentScreenTaker used for taking screenshots.
        """
        self.args = args
        self.fst = FragmentScreenTaker(args)
        self.health_bar = HealthBar()
        self.radar_status = RadarStatus()
        self.target_name = TargetName()
        self.cp_bar = CPBar()
        self.mp_bar = MPBar()
        self.tv_reader = TVReader()
        self.anti = anti

    def aggregate_screen_data(self) -> dict:
        health_bar_buffer = self.fst.take_screenshot_in_memory("health", CORDS["HEALTH"])
        health_bar_res = self.health_bar.calculate_red_bar_percentage(health_bar_buffer)

        # radar_targets_buffer = self.fst.take_screenshot_in_memory("targets", CORDS["RADAR_TARGETS"])
        # radar_targets_image = self.radar_status.load_image(radar_targets_buffer)
        # target_dots = self.radar_status.count_red_dots(radar_targets_image)
        target_dots = {'NE': 0, 'SE': 0, 'SW': 0, 'NW': 0}

        # radar_direction_buffer = self.fst.take_screenshot_in_memory("direction", CORDS["RADAR_DIRECTIONS"])
        # direction = self.radar_status.predict_direction_from_bytes(radar_direction_buffer)
        direction = 0


        target_name_buffer = self.fst.take_screenshot_in_memory("target_name",CORDS["TARGET_NAME"])
        target_name_res = self.target_name.extract_text_from_image(target_name_buffer)

        cp_bar_buffer = self.fst.take_screenshot_in_memory("cp", CORDS["CP_BAR"])
        cp_bar_data = self.cp_bar.calculate_percentage(cp_bar_buffer)
        
        mp_bar_buffer = self.fst.take_screenshot_in_memory("mp", CORDS["MP_BAR"])
        mp_bar_data = self.mp_bar.calculate_percentage(mp_bar_buffer)
        logger.debug(f"mp_bar_data: {mp_bar_data}")

        tv_buffer = self.fst.take_screenshot_in_memory("tv", CORDS["TV"])
        tv_data = self.tv_reader.extract_text_from_image(tv_buffer)

        anti_buffer = self.fst.take_screenshot_in_memory("anti", CORDS["ANTI"])
        anti_data = self.anti.extract_text_from_image(anti_buffer)

        return {
            "char_cp": cp_bar_data,
            "char_mp": mp_bar_data,
            "is_tv": tv_data,
            "is_anti": anti_data,
            "anti counter": self.anti.anti_counter,
            "health_bar": health_bar_res,
            "target_name": target_name_res,
            "target_dots": target_dots,
            "direction": direction,
        }
