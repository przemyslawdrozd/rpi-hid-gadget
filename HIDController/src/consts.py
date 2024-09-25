WS_PREFIX = "192.168.0"
PORT = 8760
WS_ERROR_TIMEOUT = 5  # Second

SERIAL_PORT = "/dev/hidg0"

# Constants for random sleep duration
# MIN_SLEEP_TIME = 0.02  # 20 milliseconds
# MAX_SLEEP_TIME = 0.05  # 50 milliseconds

MIN_SLEEP_TIME = 1
MAX_SLEEP_TIME = 5
SLEEP_TIME_RANGE = (MAX_SLEEP_TIME, MAX_SLEEP_TIME)

LOG_FORMATTING = "%(asctime)s [%(levelname)s] %(message)s"
