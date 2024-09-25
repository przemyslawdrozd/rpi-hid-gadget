NULL_CHAR = chr(0)

HID_KEY_MAP = {
    "A": (NULL_CHAR * 2 + chr(4) + NULL_CHAR * 5)
}


def get_report_value(char: str):
    return HID_KEY_MAP.get(char)
