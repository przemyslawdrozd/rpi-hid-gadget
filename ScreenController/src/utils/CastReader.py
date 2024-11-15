import logging
import pytesseract
from PIL import Image
from io import BytesIO
import pygame
import re
from ..consts import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

# INVALID_REGEX_PATTERN = r'Invalid'
# CANNOT_REGEX_PATTERN = r'Cannot'
# DISTANCE_REGEX_PATTERN = r'distance'
# MP_REGEX_PATTERN = r'Not enough MP'


class CastReader:

    def __init__(self):
        pass

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
        logger.debug(f"Cast extracted_text: {extracted_text}")
        
        if extracted_text != "":
            return True
        return False

    def __invoke_alert(self) -> None:
        # Load the sound file
        pygame.mixer.music.load(self.tv_sound_file)

        # Play the sound
        pygame.mixer.music.play()
