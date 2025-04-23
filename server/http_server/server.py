from http.server import HTTPServer
from .handler import RouterHandler
from dotenv import load_dotenv
import os

load_dotenv()

class MyHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, db):
        super().__init__(server_address, RequestHandlerClass)
        self.db = db  # share db connection here
        port = os.getenv("SERVER_PORT")
        url = os.getenv("SERVER_URL")
        self.baseUrl = f"{url}:{port}" if port else url

    def check_suns(self):
        
        return "This is check sun"

def run_http_server(db):
    try:
        server_address = (os.getenv("SERVER_URL"), int(os.getenv("SERVER_PORT")))
        print(server_address)
        httpd = MyHTTPServer(server_address, RouterHandler, db)
        print(f"🌐 Serving on http://{os.getenv('SERVER_URL')}:{os.getenv('SERVER_PORT')} (Press Ctrl+C to stop)")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        httpd.server_close()