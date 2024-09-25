import sys
import time
import asyncio
import websockets
import logging

NULL_CHAR = chr(0)

HID_KEY_MAP = {
    "A": (NULL_CHAR * 2 + chr(4) + NULL_CHAR * 5)
}


def get_report_value(char: str):
    return HID_KEY_MAP.get(char)
def write_report(report: str) -> None:
    time.sleep(0.2)
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

class HIDController:
    def __init__(self, server_ip: str, port: int = 8760):
        self.uri = f"ws://{server_ip}:{port}"
        self.websocket = None

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger("HIDController")

    async def connect(self):
        """Establish connection to the WebSocket server."""
        try:
            self.websocket = await websockets.connect(self.uri)
            self.logger.info(f"Connected to server: {self.uri}")
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            raise

    async def listen_for_messages(self):
        """Listen for messages from the WebSocket server."""
        while True:
            try:
                message = await self.websocket.recv()
                print("Receive msg:", message)
                write_report(get_report_value(message))

                write_report(NULL_CHAR * 8)
                self.logger.info(f"Received message from server: {message}")
            except websockets.ConnectionClosed:
                self.logger.warning("Connection closed, trying to reconnect...")
                break
            except Exception as e:
                self.logger.eraaror(f"Error while receiving message: {e}")
                break
    async def start(self):
        """Main loop to manage reconnections and message handling."""
        while True:
            try:
                await self.connect()
                await self.listen_for_messages()
            except Exception as e:
                self.logger.error(f"Error: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)  # Wait before attempting to reconnect


if __name__ == "__main__":

    args = sys.argv[1:]
    ws_url = args[0]

    # Replace <laptop_ip> with the actual IP address of your laptop
    hid_controller = HIDController(server_ip=ws_url)

    # Start the event loop
    asyncio.get_event_loop().run_until_complete(hid_controller.start())
