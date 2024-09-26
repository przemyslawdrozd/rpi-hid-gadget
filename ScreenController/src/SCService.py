import asyncio
from .domain.WSServer import WSServer

class SCService:
    def __init__(self):
        self.ws_client = WSServer()

    def start_sc_service(self):
        """Start the WebSocket server and manage the event loop."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ws_client.start_server())
        loop.run_forever()

