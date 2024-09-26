import asyncio
import websockets
import logging
from consts import PORT, LOGGER_NAME, WS_ERROR_TIMEOUT
from Utils import Utils

logger = logging.getLogger(LOGGER_NAME)


class HIDController:
    def __init__(self, ws_url: str):
        self.uri = f"ws://{ws_url}:{PORT}"
        self.websocket = None

    async def start(self):
        """Main loop to manage reconnections and message handling."""
        while True:
            try:
                await self.__connect()
                await self.__listen_for_messages()
            except Exception as e:
                logger.error(f"Error: {e}. Retrying in {WS_ERROR_TIMEOUT} seconds...")
                await asyncio.sleep(WS_ERROR_TIMEOUT)  # Wait before attempting to reconnect

    async def __connect(self):
        """Establish connection to the WebSocket server."""
        try:
            self.websocket = await websockets.connect(self.uri)
            logger.info(f"Connected to server: {self.uri}")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise

    async def __listen_for_messages(self):
        """Listen for messages from the WebSocket server."""
        while True:
            try:
                instructions = await self.websocket.recv()
                await Utils.handle_write_report(instructions)

                logger.info(f"Applied instructions {instructions}")

            except websockets.ConnectionClosed:
                logger.warning("Connection closed, trying to reconnect...")
                break
            except Exception as e:
                logger.error(f"Error while receiving message: {e}")
                break
