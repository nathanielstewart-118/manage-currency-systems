#!./.venv/bin/python
#coding: utf-8

import random
import os
from datetime import datetime, timedelta
import json
import cgi
import json
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="minifooko_dev",
  password="uj9Qta3b#Via",
  database="minifooko_db_dev",
  auth_plugin="mysql_native_password"
)

def log_write(mid, area, action):
    file_path = "logs/logs.json"
    new_log = {
      "mid": mid,
      "area": area,
      "action": action,
      "date": datetime.now().strftime("%Y-%m-%d")  # Current date in YYYY-MM-DD format
    }
    
    try:
        with open(file_path, "r") as file:
            # Check if the file is empty or contains invalid JSON
            file_content = file.read().strip()
            if file_content:
                logs = json.loads(file_content)
            else:
                logs = []
    except FileNotFoundError:
        # If the file doesn't exist, initialize with an empty list
        logs = []
    except json.JSONDecodeError:
        # If JSON is invalid, initialize with an empty list
        logs = []

    # Append the new log to the list
    logs.append(new_log)

    # Write the updated logs back to the file
    with open(file_path, "w") as file:
        json.dump(logs, file, indent=4)

        
def handle_withdrawal():
    try:
        form = cgi.FieldStorage()
        mid = form["mid"].value
        area = form["area"].value
        mycursor = mydb.cursor(dictionary=True)
        sql = "UPDATE mids SET deposit = 0 WHERE mid = " + mid
        mycursor.execute(sql)
        log_write(mid, area, "full withdrawal")
        mydb.commit()
        return {"message" : "Full amount withdrawn", "success": True}

    except Exception as e:
        return { "message": str(e), "success": False}
    
print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
print(json.JSONEncoder().encode(handle_withdrawal()))