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
    print(content)
    handler.send_response(200)
    handler.send_header("Content-type", "text/html")
    handler.end_headers()
    handler.wfile.write(content.encode())


def handle_post(handler, form, path):
    if path == "/admin/sun":
        command = form.get("command")
        if command == "get_suns":
            result = get_suns(handler.server.db, form)
    elif path == "/admin/log":
        result = get_logs(handler.server.db, form)
    print(path)
    return json.dumps(result, default=str)
    
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
    return {}


