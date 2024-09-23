import asyncio
import websockets

# A simple echo server
async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"Echo: {message}")

if __name__ == "__main__":
    # Bind the WebSocket server to 0.0.0.0 and port 8765
    start_server = websockets.serve(echo, "0.0.0.0", 8765)

    print("WebSocket server started at ws://0.0.0.0:8765")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
