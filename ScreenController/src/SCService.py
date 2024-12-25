import sys
import time
import asyncio
import logging
import argparse

from .domain.WSServer import WSServer
from .domain.ScreenHandler import ScreenHandler
from .domain.HIDMapper import HIDMapper
from .utils.ConsoleLog import ConsoleLog
from .utils.Anti import Anti

from .utils.VirtualKeys import press_and_release_key

from .consts import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class SCService:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.ws_client = WSServer()
        self.anti = Anti()
        self.screen_handler = ScreenHandler(self.anti, args)
        self.hid_mapper = HIDMapper(self.anti, args)
        self.cl = ConsoleLog()

    async def get_instructions(self):
        """A method to define or fetch instructions periodically."""
        logger.debug("Fetching instructions...")

        # Async
        # loop = asyncio.get_running_loop()
        # await loop.run_in_executor(None, self.screen_handler.aggregate_screen_data)

        screen_data = self.screen_handler.aggregate_screen_data()
        logger.debug(f"Aggregated screen data: {screen_data}")

        instructions, delay = await self.hid_mapper.generate_instructions(screen_data)
        self.delay = delay
        logger.debug(f"Created instructions: {instructions}")
        
        logger.debug(f"args {self.args}")
        if not self.args.debug and not self.args.mage and not self.args.ee:
            self.cl.log(screen_data, instructions)

        if self.args.screen:
            sys.exit()

        return instructions

    async def handle_broadcast_loop(self):
        """Start the broadcast and manage instructions."""
        logger.debug("Starting the broadcast loop...")
        while True:
            start_time = time.perf_counter()  # Start timing
            instructions = await self.get_instructions()
            logger.debug(f"Broadcasting instructions: {instructions}")

            if self.args.virtual:
                for instruction in instructions:
                    press_and_release_key(instruction)
            else:
                await self.ws_client.broadcast_message(instructions, self.delay)

            # control_sleep = self.hid_mapper.analise_instructions(instructions)

            # if control_sleep != 0:
            #     logger.debug("Found arrow instruction")
            #     await asyncio.sleep(control_sleep)

            # self.__apply_delay()
            exec_time = time.perf_counter() - start_time

            # Calculate remaining time to make loop execution 1 second
            # total_loop_time = 0.8  # Target loop time in seconds
            # remaining_time = total_loop_time - exec_time
            # logger.debug(f"exec_time: {exec_time:.1f}, remaining_time: {remaining_time:.1f}")

            # if remaining_time > 0:
            #     await asyncio.sleep(remaining_time)  # Add a small delay to avoid a tight loop

    async def start_sc_service(self):
        """Start the WebSocket server and manage the event loop."""

        if not self.args.virtual:
            logger.info("Starting WebSocket server...")
            await self.ws_client.start_server()
            logger.info("WebSocket server started. Entering the broadcast loop...")
        
        await self.handle_broadcast_loop()

    async def __apply_delay(self):
        await asyncio.sleep(self.delay)
        self.delay = 0