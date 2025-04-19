# server.py
import asyncio
import websockets
from dotenv import load_dotenv

load_dotenv()

async def handler(websocket, path):
    print("Client connected")
    async for message in websocket:
        print(f"Received: {message}")
        await websocket.send(f"Echo: {message}")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started at ws://localhost:8765")
        await asyncio.Future()  # run forever

asyncio.run(main())
