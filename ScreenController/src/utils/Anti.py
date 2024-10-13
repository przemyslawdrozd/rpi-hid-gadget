import logging
import pytesseract
from PIL import Image
from io import BytesIO
import pygame
import re
from ..consts import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

REGEX_PATTERN = r'anti(\w+(:\s?\w)?)?'


class Anti:

    def __init__(self):
        self.anti_sound_file = "files/anti.mp3"

        # Initialize the pygame mixer
        pygame.mixer.init()

    def extract_text_from_image(self, img_byte_arr: BytesIO) -> bool:
        """
        Extracts text from an image provided as a BytesIO object.

        Args:
            img_byte_arr (BytesIO): Image in memory from which to extract text.

        Returns:
            str: The extracted text from the image.
        """
        # Load image from BytesIO
        img_byte_arr.seek(0)  # Reset the stream position to the start
        img = Image.open(img_byte_arr)

        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(img)
        logger.debug(f"anti extracted_text: {extracted_text}")
        matches = re.findall(REGEX_PATTERN, extracted_text, re.IGNORECASE)
        logger.debug(f"anti matches: {matches}")
        result = len(matches) > 0

        if result:
            self.__invoke_alert()

        return result

    def __invoke_alert(self) -> None:
        # Load the sound file
        pygame.mixer.music.load(self.anti_sound_file)

        # Play the sound
        pygame.mixer.music.play()
