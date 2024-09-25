import time
import random
from src.HIDKeyMap import HID_KEY_MAP
from src.consts import SERIAL_PORT, SLEEP_TIME_RANGE


class Utils:
    @staticmethod
    def handle_write_report(instructions: [str]) -> None:
        """Handle all provided instructions to execute"""
        for char in instructions:
            encoded_char = Utils.get_report_value(char)
            Utils.write_report(encoded_char)
            Utils.random_sleep()

        Utils.write_report("Release")

    @staticmethod
    def write_report(report: str) -> None:
        """Write give value into serial port"""
        with open(SERIAL_PORT, "rb+") as fd:
            fd.write(report.encode())

    @staticmethod
    def get_report_value(char: str):
        """Get decoded value based on given char"""
        return HID_KEY_MAP.get(char)

    @staticmethod
    def random_sleep():
        """Sleep for a random duration between 20 and 50 milliseconds"""
        sleep_time = random.uniform(*SLEEP_TIME_RANGE)
        time.sleep(sleep_time)
