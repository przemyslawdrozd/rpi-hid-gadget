NULL_CHAR = chr(0)

HID_KEY_MAP = {
    "Release": (NULL_CHAR * 8),
    "Space": (NULL_CHAR * 2 + chr(44) + NULL_CHAR * 5),
    "Enter": (NULL_CHAR * 2 + chr(40) + NULL_CHAR * 5),
    "Esc": (NULL_CHAR * 2 + chr(41) + NULL_CHAR * 5),
    "pageUp": (NULL_CHAR * 2 + chr(74) + NULL_CHAR * 5),

    "a": (NULL_CHAR * 2 + chr(4) + NULL_CHAR * 5),
    "b": (NULL_CHAR * 2 + chr(5) + NULL_CHAR * 5),

    "F1": (NULL_CHAR * 2 + chr(58) + NULL_CHAR * 5),
    "F2": (NULL_CHAR * 2 + chr(59) + NULL_CHAR * 5),
    "F3": (NULL_CHAR * 2 + chr(60) + NULL_CHAR * 5),
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
