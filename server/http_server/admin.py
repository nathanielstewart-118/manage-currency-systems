from ..shared.utils import get_content
from pathlib import Path
import json
from dotenv import load_dotenv
import os

load_dotenv()

delay_hour = os.getenv("DELAY_HOUR")
current_file = Path(__file__)

def handle_get(handler, path):
    top_path = current_file.parent.parent.parent
    if path.find("admin/sun") > -1:
        view = top_path / "client/admin/sun.html"
    elif path.find("admin/log") > -1:
        view = top_path / 'client/admin/log.html'

    content = get_content(view)
    handler.send_response(200)
    handler.send_header("Content-type", "text/html")
    handler.end_headers()
    handler.wfile.write(content.encode())


def handle_post(handler, form, path):
    result = ""
    if path == "/admin/sun":
        command = form.get("command")
        if command == "get_suns":
            result = get_suns(handler.server.db, form)
    elif path == "/admin/logs":
        result = get_logs(handler.server.db, form)
    return result
    
def get_suns(db, form):
    cursor = db.cursor(dictionary=True)
    sql = f"SELECT * FROM suns WHERE updated_at >= DATE_SUB(NOW(), INTERVAL {delay_hour} HOUR); "
    cursor.execute(sql)
    suns = cursor.fetchall()
    
    sql = f"SELECT * FROM onetime_suns WHERE updated_at >= DATE_SUB(NOW(), INTERVAL {delay_hour} HOUR); "
    cursor.execute(sql)
    onetime_suns = cursor.fetchall()
    valid_suns = suns + onetime_suns

    sql = f"SELECT * FROM suns WHERE updated_at < DATE_SUB(NOW(), INTERVAL {delay_hour} HOUR); "
    cursor.execute(sql)
    suns = cursor.fetchall()
    
    sql = f"SELECT * FROM onetime_suns WHERE updated_at < DATE_SUB(NOW(), INTERVAL {delay_hour} HOUR); "
    cursor.execute(sql)
    onetime_suns = cursor.fetchall()
    invalid_suns = suns + onetime_suns
    print(os.getenv("DELAY_HOUR"), "-------------------------")
    return {
        "success": True,
        "data": {
            "valid_suns": valid_suns,
            "invalid_suns": invalid_suns
        }
    }

def get_logs(db, form):
    cursor = db.cursor(dictionary=True)
    date = form.get("date") or ""
    if date == "":
        return {
            "success": False,
            "messsage": "Incorrect month"
        }
    sql = f"SELECT * FROM logs WHERE created_at BETWEEN '{date}-01' AND '{date}-31 23:59:59'"
    cursor.execute(sql)
    logs = cursor.fetchall()
    return {
        "success": True,
        "logs": logs
    }


