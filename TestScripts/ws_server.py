import asyncio
import websockets

connected_clients = set()


# A simple echo server with periodic message broadcasting
async def echo(websocket, path):
    # Register the new client connection
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            await websocket.send(f"Echo: {message}")
    finally:
        # Unregister the client on disconnection
        connected_clients.remove(websocket)


async def broadcast_message():
    while True:
        if connected_clients:  # If there are any connected clients
            message = "Server message sent every 1 second"
            print("Broadcasting message to all clients")
            # Create tasks from coroutines and pass them to asyncio.wait
            tasks = [asyncio.create_task(client.send(message)) for client in connected_clients]
            await asyncio.wait(tasks)
        await asyncio.sleep(1)  # Send message every 1 second


if __name__ == "__main__":
    # Start the WebSocket server
    start_server = websockets.serve(echo, "0.0.0.0", 8760)

    print("WebSocket server started at ws://0.0.0.0:8760")

    # Schedule the server to run along with the broadcast task
    asyncio.get_event_loop().run_until_complete(start_server)

    # Run the message broadcasting task
    asyncio.get_event_loop().create_task(broadcast_message())

    # Keep the event loop running
    asyncio.get_event_loop().run_forever()
