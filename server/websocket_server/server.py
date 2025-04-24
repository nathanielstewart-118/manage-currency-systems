import asyncio
import websockets
from dotenv import load_dotenv
import os
from .handler import websocket_handler

load_dotenv()

async def run_websocket_server():
    async with websockets.serve(websocket_handler, "", int(os.getenv("SOCKET_SERVER_PORT"))):
        print(f"WebSocket server running at ws://{os.getenv("SOCKET_SERVER_URL")}:{os.getenv("SOCKET_SERVER_PORT")}")
        await asyncio.Future()  # run forever
