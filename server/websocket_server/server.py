import asyncio
import websockets
from dotenv import load_dotenv
import os
from .handler import websocket_handler

load_dotenv()

async def run_websocket_server():
    async with websockets.serve(websocket_handler, os.getenv("SOCKET_SERVER_URL"), int(os.getenv("SOCKET_SERVER_PORT"))):
        print("WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # run forever
