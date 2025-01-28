import logging
import argparse
import time

from ..utils.FragmentScreenTaker import FragmentScreenTaker
from ..utils.HealthBar import HealthBar
from ..utils.RadarStatus import RadarStatus
from ..utils.TargetName import TargetName
from ..utils.CPBar import CPBar
from ..utils.MPBar import MPBar
from ..utils.HPBar import HPBar
from ..utils.TVReader import TVReader
from ..utils.ChatReader import ChatReader
from ..utils.CastReader import CastReader
from ..utils.Anti import Anti

from ..consts import LOGGER_NAME, CORDS

logger = logging.getLogger(LOGGER_NAME)


class ScreenHandler:
    def __init__(self, anti: Anti, args: argparse.Namespace):
        """
        Initialize the ScreenHandler with a FragmentScreenTaker instance.
        :param fragment screen-taker: Instance of FragmentScreenTaker used for taking screenshots.
        """
        self.args = args
        self.fst = FragmentScreenTaker(args)
        self.health_bar = HealthBar()
        # self.radar_status = RadarStatus()
        self.target_name = TargetName()
        self.cp_bar = CPBar()
        self.hp_bar = HPBar(152)
        self.mp_bar = MPBar(115)
        self.pt_hp_bar = HPBar(140)
        self.pt_mp_bar = MPBar(126)
        self.member_stat = None
        # self.tv_reader = TVReader()
        self.chat = ChatReader()
        # self.cast = CastReader()
        self.anti = anti

    def aggregate_screen_data(self) -> dict:
        start_time = time.perf_counter()
        
        health_start = time.perf_counter()
        health_bar_buffer = self.fst.take_screenshot_in_memory("health", CORDS["HEALTH"])
        health_bar_res = self.health_bar.calculate_red_bar_percentage(health_bar_buffer)
        health_end = time.perf_counter()
        logger.debug(f"SCREEN Health bar processing time: {health_end - health_start:.4f} seconds")

        # Skipped radar processing steps, using dummy data
        target_dots = {'NE': 0, 'SE': 0, 'SW': 0, 'NW': 0}
        direction = 0

        # target_name_start = time.perf_counter()
        # target_name_buffer = self.fst.take_screenshot_in_memory("target_name", CORDS["TARGET_NAME"])
        # target_name_res = self.target_name.extract_text_from_image(target_name_buffer)
        # target_name_end = time.perf_counter()
        # logger.debug(f"SCREEN Target name processing time: {target_name_end - target_name_start:.4f} seconds")

        cp_start = time.perf_counter()
        cp_bar_buffer = self.fst.take_screenshot_in_memory("cp", CORDS["CP_BAR"])
        cp_bar_data = self.cp_bar.calculate_percentage(cp_bar_buffer)
        cp_end = time.perf_counter()
        logger.debug(f"SCREEN CP bar processing time: {cp_end - cp_start:.4f} seconds")
        
        mp_start = time.perf_counter()
        mp_bar_buffer = self.fst.take_screenshot_in_memory("mp", CORDS["MP_BAR"])
        mp_bar_data = self.mp_bar.calculate_percentage(mp_bar_buffer)
        mp_end = time.perf_counter()
        logger.debug(f"SCREEN MP bar processing time: {mp_end - mp_start:.4f} seconds")

        hp_start = time.perf_counter()
        hp_bar_buffer = self.fst.take_screenshot_in_memory("hp", CORDS["HP_BAR"])
        hp_bar_data = self.hp_bar.calculate_percentage(hp_bar_buffer)
        hp_end = time.perf_counter()
        logger.debug(f"SCREEN HP bar processing time: {hp_end - hp_start:.4f} seconds")
        
        pt_mp_bar_data = None
        pt_hp_bar_data = None
        if self.args.ee:
            pt_mp_start = time.perf_counter()
            pt_mp_bar_buffer = self.fst.take_screenshot_in_memory("pt_mp", CORDS["PT_MP_BAR"])
            pt_mp_bar_data = self.pt_mp_bar.calculate_percentage(pt_mp_bar_buffer)
            pt_mp_end = time.perf_counter()
            logger.debug(f"SCREEN MP bar processing time: {pt_mp_end - pt_mp_start:.4f} seconds")

            pt_hp_start = time.perf_counter()
            pt_hp_bar_buffer = self.fst.take_screenshot_in_memory("pt_hp", CORDS["PT_HP_BAR"])
            pt_hp_bar_data = self.pt_hp_bar.calculate_percentage(pt_hp_bar_buffer)
            pt_hp_end = time.perf_counter()
            logger.debug(f"SCREEN HP bar processing time: {pt_hp_end - pt_hp_start:.4f} seconds")

        # tv_start = time.perf_counter()
        # tv_buffer = self.fst.take_screenshot_in_memory("tv", CORDS["TV"])
        # tv_data = self.tv_reader.extract_text_from_image(tv_buffer)
        # tv_end = time.perf_counter()
        # logger.debug(f"SCREEN TV data processing time: {tv_end - tv_start:.4f} seconds")

        chat_start = time.perf_counter()
        chat_buffer = self.fst.take_screenshot_in_memory("chat", CORDS["CHAT"])
        chat_data = self.chat.extract_text_from_image(chat_buffer)
        chat_end = time.perf_counter()
        logger.debug(f"SCREEN Chat data processing time: {chat_end - chat_start:.4f} seconds")

        if self.args.anti:
            anti_start = time.perf_counter()
            anti_buffer = self.fst.take_screenshot_in_memory("anti", CORDS["ANTI"])
            anti_data = self.anti.extract_text_from_image(anti_buffer)
            anti_end = time.perf_counter()
            logger.debug(f"SCREEN Anti data processing time: {anti_end - anti_start:.4f} seconds")
        else:
            anti_data = False

        end_time = time.perf_counter()
        logger.debug(f"SCREEN Total processing time: {end_time - start_time:.4f} seconds")

        return {
            "char_cp": cp_bar_data,
            "char_mp": mp_bar_data,
            "char_hp": hp_bar_data,
            # "is_tv": tv_data,
            "is_tv": False,
            "is_anti": anti_data,
            # "is_anti": False,
            # "anti counter": self.anti.anti_counter,
            "chat": chat_data,
            "health_bar": health_bar_res,
            # "target_name": target_name_res,
            "target_name": "",
            "target_dots": target_dots,
            "direction": direction,
            "pt_mp": pt_mp_bar_data,
            "pt_hp": pt_hp_bar_data,
        }