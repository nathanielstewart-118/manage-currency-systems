from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
from datetime import datetime

from . import owners, com, admin
from ..shared.utils import authorize_terminal
class RouterHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        # print("A request is made" + client_address)
        
    def do_GET(self):
        # print(f"A request is made {self.client_address}")
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        # Route based on URL
        
        if path.find("owners") > -1:
            owners.handle_get(self, path)
        elif path.find("admin") > -1:
            admin.handle_get(self, path)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        print("This is handle post")
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        form = json.loads(post_data)
        tid = form.get("tid")
        token = form.get("token")
        auth = form.get('auth')
        
        if token is None:
            token = auth
        if authorize_terminal(tid, token, self) == False:
            return
        print("This is after authorize")
        result = "{}"
        if path == "/com":
            result = com.handle(form, self)
        elif path.find("owners") > -1:
            result = owners.handle_post(self, form)
        elif path.find("admin") > -1:
            result = admin.handle_post(self, form, path)
            
        db = self.server.db
        cursor = db.cursor(dictionary=True)
        tid = form.get("tid") or ""
        command = form.get("command") or ""
        ip_address = self.client_address[0] or ""
        sql = f"INSERT INTO logs(ip_address, tid, command, received_json, sent_json, created_at, updated_at) VALUES('{ip_address}', '{tid}', '{command}', '{post_data}', '{result}', '{datetime.now()}', '{datetime.now()}')"
        cursor.execute(sql)
        db.commit()
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(result.encode())


