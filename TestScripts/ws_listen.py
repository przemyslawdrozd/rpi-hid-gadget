import asyncio
import websockets

async def listen_messages(uri):
    async with websockets.connect(uri) as websocket:
        print("Listening for messages...")
        async for message in websocket:
            print(f"Received message: {message}")

if __name__ == "__main__":
    uri = "ws://localhost:8765"  # Local WebSocket server URI

    asyncio.get_event_loop().run_until_complete(listen_messages(uri))