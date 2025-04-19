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
  user="root",
  password="",
  database="atm_service",
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


def handle_cancelWithdrawal():
    try:
        form = cgi.FieldStorage()
        mid = form["mid"].value
        amount = form["amount"].value
        area = form["area"].value
        mycursor = mydb.cursor()

        sql = "UPDATE mids SET deposit = deposit + " + amount + " WHERE mid = "+ mid
        mycursor.execute(sql)
        log_write(mid, area, "cancel deposit amount:" + amount)
        mydb.commit()
        return {"message": "Invoice cancelled", "success": True}
    
    except Exception as e:
        return { "message": str(e), "success": False}
    
print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
print(json.JSONEncoder().encode(handle_cancelWithdrawal()))
