import asyncio
import logging

from .domain.WSServer import WSServer
from .domain.ScreenHandler import ScreenHandler
from .consts import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class SCService:
    def __init__(self):
        self.ws_client = WSServer()
        self.screen_handler = ScreenHandler()

    async def get_instructions(self):
        """A method to define or fetch instructions periodically."""
        logger.info("Fetching instructions...")

        # Async
        # loop = asyncio.get_running_loop()
        # await loop.run_in_executor(None, self.screen_handler.aggregate_screen_data)

        data = self.screen_handler.aggregate_screen_data()
        # data = ["F1", "F2"]

        logger.debug(f"Aggregated screen data: {data}")
        return data

    async def handle_broadcast_loop(self):
        """Start the broadcast and manage instructions."""
        logger.info("Starting the broadcast loop...")
        while True:
            instructions = await self.get_instructions()
            logger.debug(f"Broadcasting instructions: {instructions}")
            await self.ws_client.broadcast_message(instructions)
            await asyncio.sleep(1)  # Add a small delay to avoid a tight loop

    async def start_sc_service(self):
        """Start the WebSocket server and manage the event loop."""
        logger.info("Starting WebSocket server...")
        await self.ws_client.start_server()  # Start the WebSocket server
        logger.info("WebSocket server started. Entering the broadcast loop...")
        await self.handle_broadcast_loop()  # Run the broadcast loop