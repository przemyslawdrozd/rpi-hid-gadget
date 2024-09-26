import random
import asyncio
import logging
import aiofiles

from HIDKeyMap import HID_KEY_MAP
from consts import SERIAL_PORT, SLEEP_TIME_RANGE, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class Utils:
    @staticmethod
    async def handle_write_report(instructions: [str]) -> None:
        """Handle all provided instructions to execute"""
        for char in instructions:
            logger.debug(f"Iter {char}")
            encoded_char = Utils.get_report_value(char)
            logger.debug("Found encoded_char")
            await Utils.write_report(encoded_char)
            await Utils.random_sleep()

        logger.debug("Release..")
        await Utils.write_report("Release")

    @staticmethod
    async def write_report(report: str) -> None:
        """Asynchronously write the given value into serial port"""
        async with aiofiles.open(SERIAL_PORT, "rb+") as fd:
            await fd.write(report.encode())

    @staticmethod
    def get_report_value(char: str):
        """Get decoded value based on given char"""
        return HID_KEY_MAP.get(char)

    @staticmethod
    async def random_sleep():
        """Sleep for a random duration between 20 and 50 milliseconds"""
        sleep_time = random.uniform(*SLEEP_TIME_RANGE)
        logger.debug(f"sleep_time: {sleep_time}")
        await asyncio.sleep(sleep_time)

