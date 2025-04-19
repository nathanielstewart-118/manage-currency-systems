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
        mycursor = mydb.cursor(dictionary=True)

        form = cgi.FieldStorage()
        sun = form["sun"].value
        area = form["area"].value
        deposit_value = form["deposit_value"].value
        service_type = form["service_type"].value

        sql = "SELECT * FROM suns WHERE sun = " + sun
        mycursor.execute(sql)
        sun_data = mycursor.fetchone()
        if not sun_data:
            return { "message": "No SUN", "success": False}
        
        sql = "SELECT * FROM mids WHERE mid = "+ sun_data['mid']
        mycursor.execute(sql)
        mid_data = mycursor.fetchone()
        
        if mid_data["deposit"] <= 0:
            return { "message": "No Deposit", "success": False}
        
        if service_type == "IMMEDIATE":
            sql = "UPDATE mids SET deposit = deposit - " + deposit_value + " WHERE mid = " + sun_data['mid']
            mycursor.execute(sql)
            sql = "SELECT * FROM mids WHERE mid = " + sun_data['mid']
            mycursor.execute(sql)
            remain_data = mycursor.fetchone()
            log_write(sun_data['mid'], area, service_type + ":" + deposit_value)
            mydb.commit()

            return {"message" : "Thank you", "remain": remain_data['deposit'], "success": True}

        if service_type == "PAYAFTERSERVICE" and int(mid_data['deposit']) < int(deposit_value):
            shortfall = int(deposit_value) - int(mid_data['deposit'])
            sql = "UPDATE mids SET deposit = 0 WHERE mid = "+ sun_data['mid']
            mycursor.execute(sql)
            sql = "UPDATE suns SET expire_date = NOW() WHERE sun = "+ sun
            mycursor.execute(sql)
            log_write(sun_data['mid'], area, service_type + ":" + deposit_value)
            mydb.commit()
            return {"message": "Invoice processed with shortfall", "shortfall": shortfall, "success": True}
        else:
            sql = "UPDATE mids SET deposit = deposit - " + deposit_value + " WHERE mid=" + sun_data['mid']
            mycursor.execute(sql)
            remain = int(mid_data["deposit"]) - int(deposit_value)
            log_write(sun_data['mid'], area, deposit_value)
            return {"message": "Invoice processed", "remain": remain, "success": True}

    except Exception as e:
        return { "message": str(e), "success": False}
    
print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
print(json.JSONEncoder().encode(handle_withdrawal()))