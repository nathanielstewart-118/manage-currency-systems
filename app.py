import asyncio
import threading
from dotenv import load_dotenv
import os
import mysql.connector

from server.http_server import admin
from server.http_server.server import run_http_server
from server.websocket_server.server import run_websocket_server
from server.tasks.scheduler import start_scheduler

load_dotenv()

async def main():  
    db = mysql.connector.connect(
        host=os.getenv("DB_URL"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        auth_plugin="mysql_native_password"
    )
    # HTTP server runs in a separate thread
    threading.Thread(target=start_scheduler, args=(db, ), daemon=True).start()

    threading.Thread(target=run_http_server, args=(db, ), daemon=True).start()
    # threading.Thread(target=run_websocket_server, daemon=True).start()
    # run_http_server()
    # WebSocket server runs on asyncio event loop
    # asyncio.run(run_websocket_server())
    await run_websocket_server()

if __name__ == "__main__":
    asyncio.run(main())
    
    

    