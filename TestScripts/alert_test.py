import pygame
import time

# Initialize the pygame mixer
pygame.mixer.init()

# Load the sound file
sound_file = "../ScreenController/files/cp.mp3"  # Replace with your sound file path
pygame.mixer.music.load(sound_file)

# Play the sound
pygame.mixer.music.play()

# Wait until the sound finishes playing
while pygame.mixer.music.get_busy():
    time.sleep(1)

print("Sound playback finished.")
