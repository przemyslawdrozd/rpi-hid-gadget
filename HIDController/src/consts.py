WS_PREFIX = "192.168.0"
PORT = 8760
WS_ERROR_TIMEOUT = 5  # Second

SERIAL_PORT = "/dev/hidg0"

# Constants for random sleep duration
MIN_SLEEP_TIME = 0.05  # 50 milliseconds
MAX_SLEEP_TIME = 0.1  # 50 milliseconds
SLEEP_TIME_RANGE = (MIN_SLEEP_TIME, MAX_SLEEP_TIME)

LOGGER_NAME = "HIDController"
LOG_FORMATTING = "%(asctime)s [%(levelname)s] %(message)s"
