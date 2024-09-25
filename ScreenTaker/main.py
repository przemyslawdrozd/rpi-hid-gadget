import sys

from domain.WSServer import WSServer


def main():
    ws_server = WSServer()
    ws_server.start()


if __name__ == "__main__":
    main()
