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

HID_KEY_MAP = {
    "Release": 0x00,
    "Space": 0x20,         # Virtual-Key Code for Space
    "Enter": 0x0D,         # Virtual-Key Code for Enter

    # Alphabet keys
    "a": 0x41,             # Virtual-Key Code for 'A'
    "b": 0x42,             # Virtual-Key Code for 'B'
    
    # Function keys (F1-F12)
    "F1": 0x70,            # Virtual-Key Code for F1
    "F2": 0x71,            # Virtual-Key Code for F2
    "F3": 0x72,            # Virtual-Key Code for F3
    "F4": 0x73,            # Virtual-Key Code for F4
    "F5": 0x74,            # Virtual-Key Code for F5
    "F6": 0x75,            # Virtual-Key Code for F6
    "F7": 0x76,            # Virtual-Key Code for F7
    "F8": 0x77,            # Virtual-Key Code for F8
    "F9": 0x78,            # Virtual-Key Code for F9
    "F10": 0x79,           # Virtual-Key Code for F10
    "F11": 0x7A,           # Virtual-Key Code for F11
    "F12": 0x7B,           # Virtual-Key Code for F12

    # Arrow keys
    "a_up": 0x26,          # Virtual-Key Code for Up Arrow
    "a_down": 0x28,        # Virtual-Key Code for Down Arrow
    "a_left": 0x25,        # Virtual-Key Code for Left Arrow
    "a_right": 0x27        # Virtual-Key Code for Right Arrow
}

# Press and release a key, using the Virtual-Key Code (e.g., 0x72 for F3)
def press_and_release_key(key):

    vk_code = HID_KEY_MAP[key]
    print("Got VK", key, vk_code)
    press_key(vk_code)  # Press the key
    time.sleep(0.05)    # Short delay
    release_key(vk_code)  # Release the key