import time
NULL_CHAR = chr(0)

time.sleep(2)


def write_report(report) -> None:
    time.sleep(0.2)
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())


# Press F1
write_report(NULL_CHAR * 2 + chr(58) + NULL_CHAR * 5)

# Press F2
write_report(NULL_CHAR * 2 + chr(59) + NULL_CHAR * 5)

# Release all keys
write_report(NULL_CHAR*8)