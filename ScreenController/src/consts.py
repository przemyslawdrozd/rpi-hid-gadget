LOGGER_NAME = "ScreenController"
LOG_FORMATTING = "%(asctime)s [%(levelname)s] %(message)s"


HEALTH_BAR_PREFIX = 66
CP_PREFIX = 170

# Cords
HEALTH = {"L": 775, "T": 53, "W": 360, "H": 7}
# RADAR_TARGETS = {"L": 1472, "T": 40, "W": 200, "H": 200}

# HB
# RADAR_TARGETS = {"L": 1520, "T": 90, "W": 100, "H": 100}
RADAR_TARGETS = {"L": 1550, "T": 118, "W": 60, "H": 60}
RADAR_DIRECTIONS = {"L": 1552, "T": 115, "W": 60, "H": 60}
TARGET_NAME = {"L": 850, "T": 30, "W": 250, "H": 25}
CP_BAR = {"L": 200, "T": 60, "W": 175, "H": 8}
TV = {"L": 805, "T": 375, "W": 70, "H": 20}
ANTI = {"L": 700, "T": 390, "W": 200, "H": 40}

# Virtual
# HEALTH = {"L": 775, "T": 53, "W": 360, "H": 7}
# RADAR_TARGETS = {"L": 1472, "T": 40, "W": 200, "H": 200}
# RADAR_DIRECTIONS = {"L": 1542, "T": 105, "W": 60, "H": 60}
# TARGET_NAME = {"L": 850, "T": 30, "W": 250, "H": 25}
# CP_BAR = {"L": 200, "T": 60, "W": 175, "H": 8}
# TV = {"L": 805, "T": 375, "W": 70, "H": 20}
# ANTI = {"L": 700, "T": 390, "W": 200, "H": 40}

CORDS = {
    "HEALTH": HEALTH,
    "RADAR_TARGETS": RADAR_TARGETS,
    "RADAR_DIRECTIONS": RADAR_DIRECTIONS,
    "TARGET_NAME": TARGET_NAME,
    "CP_BAR": CP_BAR,
    "TV": TV,
    "ANTI": ANTI,
}
