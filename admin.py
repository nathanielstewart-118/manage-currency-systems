#!./venv/bin/python3
#coding: utf-8

from dotenv import load_dotenv
import os
import sys
import json
import cgi
from datetime import datetime, timedelta
from dotenv import load_dotenv
import mysql.connector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../', 'shared')))
from utils import gen_sun, get_content, gen_barcode


load_dotenv()

delay_hour = os.getenv("DELAY_HOUR")


db = mysql.connector.connect(
    host=os.getenv("DB_URL"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    auth_plugin="mysql_native_password"
)


def handle_post():
    form = cgi.FieldStorage()
    command = form["command"].value
    if command == "get_suns":
        result = get_suns(db)
    elif command ==  "get_logs":
        result = get_logs(db, form)
    else: 
        result = ""
    print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
    print(json.dumps(result, default=str))   
    
def get_suns(db):
    cursor = db.cursor(dictionary=True)
    sql = f"SELECT * FROM suns WHERE updated_at >= DATE_SUB(NOW(), INTERVAL {delay_hour} HOUR); "
    cursor.execute(sql)
    suns = cursor.fetchall()
    
    sql = f"SELECT onetime_sun, tid, owner_sun, created_at, updated_at, expired_at FROM onetime_suns WHERE updated_at >= DATE_SUB(NOW(), INTERVAL {delay_hour} HOUR); "
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
    return {
        "success": True,
        "data": {
            "valid_suns": valid_suns,
            "invalid_suns": invalid_suns
        }
    }

def get_logs(db, form):
    cursor = db.cursor(dictionary=True)
    date = form["date"].value or ""
    if date == "":
        return {
            "success": False,
            "messsage": "Incorrect month"
        }
        
    first_day = datetime.strptime(date, "%Y-%m")
    next_month = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1)

    sql = f"SELECT ip_address, tid, command, received_json, sent_json, created_at, updated_at FROM logs WHERE created_at BETWEEN '{first_day.strftime("%Y-%m-%d")} 00:00:00' AND '{next_month.strftime("%Y-%m-%d")} 00:00:00'"
    # sql = f"SELECT ip_address, tid, command, received_json, sent_json, created_at, updated_at FROM logs"
    
    cursor.execute(sql)
    logs = cursor.fetchall()
    return {
        "success": True,
        "logs": logs
    }

handle_post()