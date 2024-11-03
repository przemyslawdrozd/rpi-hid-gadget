import ctypes
import time

# Define necessary constants and structures
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),  # Virtual key code
                ("wScan", ctypes.c_ushort),  # Hardware scan code
                ("dwFlags", ctypes.c_ulong),  # Flags (0 for key press, KEYEVENTF_KEYUP for key release)
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Function to press a key
def press_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0, 0, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Function to release a key
def release_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0, 0x0002, 0, ctypes.pointer(extra))  # 0x0002 is KEYEVENTF_KEYUP
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Press and release a key, using the Virtual-Key Code (e.g., 0x72 for F3)
def press_and_release_key(vk_code):
    press_key(vk_code)  # Press the key
    time.sleep(0.05)    # Short delay
    release_key(vk_code)  # Release the key

# Virtual-Key Code for F3
VK_F3 = 0x72

# Mapping for common key virtual codes
VK_A = 0x41


NULL_CHAR = chr(0)
HID_KEY_MAP = {
    "Release": (NULL_CHAR * 8),
    "Space": (NULL_CHAR * 2 + chr(44) + NULL_CHAR * 5),
    "Enter": (NULL_CHAR * 2 + chr(40) + NULL_CHAR * 5),

    "a": (NULL_CHAR * 2 + chr(4) + NULL_CHAR * 5),
    "b": (NULL_CHAR * 2 + chr(5) + NULL_CHAR * 5),

    "F1": (NULL_CHAR * 2 + chr(58) + NULL_CHAR * 5),
    "F2": (NULL_CHAR * 2 + chr(59) + NULL_CHAR * 5),
    "F3": 0x72,
    "F4": (NULL_CHAR * 2 + chr(61) + NULL_CHAR * 5),
    "F5": (NULL_CHAR * 2 + chr(62) + NULL_CHAR * 5),
    "F6": (NULL_CHAR * 2 + chr(63) + NULL_CHAR * 5),
    "F7": (NULL_CHAR * 2 + chr(64) + NULL_CHAR * 5),
    "F8": (NULL_CHAR * 2 + chr(65) + NULL_CHAR * 5),
    "F9": (NULL_CHAR * 2 + chr(66) + NULL_CHAR * 5),
    "F10": (NULL_CHAR * 2 + chr(67) + NULL_CHAR * 5),
    "F11": (NULL_CHAR * 2 + chr(68) + NULL_CHAR * 5),
    "F12": (NULL_CHAR * 2 + chr(69) + NULL_CHAR * 5),

    "a_up": (NULL_CHAR * 2 + chr(82) + NULL_CHAR * 5),
    "a_down": (NULL_CHAR * 2 + chr(81) + NULL_CHAR * 5),
    "a_left": (NULL_CHAR * 2 + chr(80) + NULL_CHAR * 5),
    "a_right": (NULL_CHAR * 2 + chr(79) + NULL_CHAR * 5)
}


if __name__ == "__main__":
    time.sleep(2)  # Give yourself time to focus on the target window (e.g., Notepad)

    # Example: Press and release the F3 key
    press_and_release_key(HID_KEY_MAP["F3"])
