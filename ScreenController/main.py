import sys
import time
import logging
import asyncio
import argparse
from src.SCService import SCService
from src.consts import LOGGER_NAME, LOG_FORMATTING
import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

logger = logging.getLogger(LOGGER_NAME)


def set_logger(debug_mode=False):
    # Set default log level to INFO
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logger.setLevel(log_level)

    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(LOG_FORMATTING)
    formatter.converter = time.gmtime
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.parent = False


async def main_async(args: argparse.Namespace):
    logger.info("Init service")
    service = SCService(args)

    logger.info("Start screen controller service")
    await service.start_sc_service()

    logger.info("Stop service")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the screen controller service")

    parser.add_argument("-debug", action="store_true", help="Run in debug mode")
    parser.add_argument("-screen", action="store_true", help="Run in screen mode")
    parser.add_argument("-assist", action="store_true", help="Run in assist mode")
    parser.add_argument("-it", action="store_true", help="Run in assist mode")
    parser.add_argument("-virtual", action="store_true", help="Run in virtual mode")
    parser.add_argument("-ms", action="store_true", help="Run in mage short mode")
    parser.add_argument("-mage", action="store_true", help="Run in mage general mode")
    parser.add_argument("-male", action="store_true", help="Run in mage general mode")
    parser.add_argument("-arch", action="store_true", help="Run in archer boost mode")
    parser.add_argument("-spoil", action="store_true", help="Run in spoil mode")
    parser.add_argument("-ee", action="store_true", help="Run in mage general mode")
    parser.add_argument("-anti", action="store_true", help="Enable anti mode")

    args = parser.parse_args()

    # Set logger based on debug argument
    set_logger(debug_mode=args.debug)

    # Start the async event loop
    asyncio.run(main_async(args))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.info(f"Closed {e}")
