import asyncio
import websockets
from websockets.asyncio.server import broadcast
import json


connected_clients = set()
async def websocket_handler(websocket):
    connected_clients.add(websocket)
    # await websocket.send(json.dumps({"msg": "Hi, welcome!"}))
    print("new connections")
    try:
        async for message in websocket:
            print(f"WebSocket received: {message}")
            await websocket.send(f"Echo: {message}")
    except Exception as e:
        print(e)
    finally:
        connected_clients.remove(websocket)

async def send_to_all(msg):
    print(connected_clients)
    broadcast(connected_clients, msg)