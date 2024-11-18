import logging
import pytesseract
from PIL import Image
from io import BytesIO
import pygame
import re
from ..consts import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class HPAlarm:

    def __init__(self):
        self.tv_sound_file = "files/tv.mp3"

        # Initialize the pygame mixer
        pygame.mixer.init()

 
    def invoke_alert(self) -> None:
        # Load the sound file
        pygame.mixer.music.load(self.tv_sound_file)

        # Play the sound
        pygame.mixer.music.play()
