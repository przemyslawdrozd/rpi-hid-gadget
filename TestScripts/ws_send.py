import asyncio
import websockets


async def send_message(uri, message):
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        print(f"Sent message: {message}")


if __name__ == "__main__":
    uri = "ws://localhost:8765"  # Local WebSocket server URI
    message = "Hello from local sender!"

    asyncio.get_event_loop().run_until_complete(send_message(uri, message))
