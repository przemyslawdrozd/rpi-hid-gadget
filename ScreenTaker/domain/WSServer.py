import asyncio
import websockets

PORT = 8760
HOST = "0.0.0.0"
class WSServer:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.connected_clients = set()
        self.server = None

    async def handle_client(self, websocket, path):
        """Handle incoming messages from clients and send echo responses."""
        # Register the new client connection
        self.connected_clients.add(websocket)
        try:
            async for message in websocket:
                print(f"Received message: {message}")
                await websocket.send(f"Echo: {message}")
        finally:
            # Unregister the client on disconnection
            self.connected_clients.remove(websocket)

    async def broadcast_message(self):
        """Broadcast a periodic message to all connected clients."""
        while True:
            if self.connected_clients:  # If there are any connected clients

                NULL_CHAR = chr(0)

                message = "A"

                print("encoded message F1", )
                print("Broadcasting message to all clients")


                tasks = [asyncio.create_task(client.send(message)) for client in self.connected_clients]
                await asyncio.wait(tasks)
            await asyncio.sleep(1)  # Send message every 1 second

    def start(self):
        """Start the WebSocket server and run the broadcast task."""
        # Create the WebSocket server
        self.server = websockets.serve(self.handle_client, self.host, self.port)
        print(f"WebSocket server started at ws://{self.host}:{self.port}")

        # Run the server and the broadcast message task
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.server)
        loop.create_task(self.broadcast_message())
        loop.run_forever()
