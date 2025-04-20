from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
from datetime import datetime

from . import owners, com, admin
from ..shared.utils import authorize_terminal, send_response
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
        try:
            print("This is handle post")
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            form = json.loads(post_data)
            tid = form.get("tid") or ""
            token = form.get("token") or form.get('auth') or ""
            command = form.get("command") or ""
            if command not in ["refresh_db", "get_logs", "reqtoken", "reqconfig", "save_max_sales_amount"] and authorize_terminal(tid, token, self) == False:
                return
            print("This is after authorize")
            result = ""
            if path == "/com":
                result = com.handle(form, self)
            elif path.find("owners") > -1:
                result = owners.handle_post(self, form)
            elif path.find("admin") > -1:
                result = admin.handle_post(self, form, path)
            print(result)
            json_result = json.dumps(result, default=str)    
            db = self.server.db
            cursor = db.cursor(dictionary=True)
            tid = form.get("tid") or ""
            command = form.get("command") or ""
            ip_address = self.client_address[0] or ""
            sql = "INSERT INTO logs(ip_address, tid, command, received_json, sent_json, created_at, updated_at) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            values = (ip_address, tid, command, post_data, json_result, str(datetime.now()), str(datetime.now()))
            cursor.execute(sql, values)
            db.commit()
            
            send_response(self, 200, "application/json", json_result.encode())
        except Exception as e:
            print(e)
            data = { "success": False, "message": str(e)}
            send_response(self, 200, "application/json", json.dumps(data).encode())

