import time
import asyncio
import logging

from .domain.WSServer import WSServer
from .domain.ScreenHandler import ScreenHandler
from .domain.HIDMapper import HIDMapper
from .consts import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class SCService:
    def __init__(self):
        self.ws_client = WSServer()
        self.screen_handler = ScreenHandler()
        self.hid_mapper = HIDMapper()

    async def get_instructions(self):
        """A method to define or fetch instructions periodically."""
        logger.info("Fetching instructions...")

        # Async
        # loop = asyncio.get_running_loop()
        # await loop.run_in_executor(None, self.screen_handler.aggregate_screen_data)

        screen_data = self.screen_handler.aggregate_screen_data()
        logger.debug(f"Aggregated screen data: {screen_data}")

        instructions = self.hid_mapper.generate_instructions(screen_data)
        logger.debug(f"Created instructions: {instructions}")

        return instructions

    async def handle_broadcast_loop(self):
        """Start the broadcast and manage instructions."""
        logger.info("Starting the broadcast loop...")
        while True:
            start_time = time.perf_counter()  # Start timing
            instructions = await self.get_instructions()
            logger.debug(f"Broadcasting instructions: {instructions}")

            await self.ws_client.broadcast_message(instructions)

            control_sleep = self.hid_mapper.analise_instructions(instructions)

            if control_sleep != 0:
                logger.debug("Found arrow instruction")
                await asyncio.sleep(control_sleep)

            exec_time = time.perf_counter() - start_time

            # Calculate remaining time to make loop execution 1 second
            total_loop_time = 1.0  # Target loop time in seconds
            remaining_time = total_loop_time - exec_time
            logger.debug(f"exec_time: {exec_time:.1f}, remaining_time: {remaining_time:.1f}")

            if remaining_time > 0:
                await asyncio.sleep(remaining_time)  # Add a small delay to avoid a tight loop

    async def start_sc_service(self):
        """Start the WebSocket server and manage the event loop."""
        logger.info("Starting WebSocket server...")
        await self.ws_client.start_server()
        logger.info("WebSocket server started. Entering the broadcast loop...")
        await self.handle_broadcast_loop()
