import asyncio
import logging
import websockets

PORT = 8760
HOST = "0.0.0.0"


class WSServer:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.connected_client = None  # Only one client at a time
        self.server = None

    async def handle_client(self, websocket, path):
        """Handle incoming messages from the single connected client and send echo responses."""
        if self.connected_client is not None:
            # Reject any new connection if there's already a connected client
            await websocket.close(code=1013, reason="Another client is already connected.")
            return

        # Register the client
        self.connected_client = websocket
        try:
            async for message in websocket:
                print(f"Received message: {message}")
                await websocket.send(f"Echo: {message}")
        finally:
            # Unregister the client on disconnection
            self.connected_client = None

    async def broadcast_message(self):
        """Broadcast a periodic message to the connected client."""
        while True:
            if self.connected_client:  # If there's a connected client
                instructions = ["a", "b"]
                logging.info(f"Send instructions {instructions}")
                print("elko", instructions)
                try:
                    await self.connected_client.send(instructions)
                except websockets.exceptions.ConnectionClosed:
                    self.connected_client = None
            await asyncio.sleep(1)  # Send message every 1 second

    async def start_server(self):
        """Start the WebSocket server and run the broadcast message task."""
        self.server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"WebSocket server started at ws://{self.host}:{self.port}")
        await self.broadcast_message()
