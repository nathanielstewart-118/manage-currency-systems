#!./.venv/bin/python
#coding: utf-8

import random
import os
from datetime import datetime, timedelta
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


def handle_inquiry():
    try:
        form = cgi.FieldStorage()
        mid = form["mid"].value
        area = form["area"].value
        sun_duration = 24
        mycursor = mydb.cursor(dictionary=True)
        if not mid:
            return { "message": "missing MID", "success": False}
        sql = "SELECT * FROM mids WHERE mid ="+ mid
        mycursor.execute(sql)
        result = mycursor.fetchone()
        result["issue_date"] = result["issue_date"].strftime('%Y-%m-%d %H:%M:%S') if result["issue_date"] else None
        
        if not result:
            return { "message": "MID not found", "success": False}
        
        sql = "SELECT * FROM suns WHERE mid = " + mid + " AND expire_date > NOW()"
        mycursor.execute(sql)
        sun = mycursor.fetchone()
        if sun is None:
            new_sun = f"{random.randint(10**7, 10**8 - 1)}"
            sun_expire_date = datetime.now() + timedelta(hours=sun_duration)
            sql = "INSERT INTO suns (mid, sun, expire_date) VALUES (%s, %s, %s)"
            mycursor.execute(sql, (mid, new_sun, sun_expire_date))
            sun["expire_date"] = sun_expire_date.strftime('%Y-%m-%d %H:%M:%S') if sun["expire_date"] else None
            print(sun["expire_date"])

        else:
            sun["expire_date"] = sun["expire_date"].strftime('%Y-%m-%d %H:%M:%S') if sun["expire_date"] else None 
        sql = "DELETE FROM suns WHERE mid = '"+ mid +"' AND expire_date < NOW()"
        mycursor.execute(sql)
        log_write(mid, area, "inquiry")
        mydb.commit()
        return {
                "MID": result["mid"],
                "issue_date": result["issue_date"],
                "deposit": result["deposit"],
                "SUN": sun["sun"] if sun else None,
                "SUN_expire_date": sun["expire_date"] if sun else None, 
                "success": True}
        
    except Exception as e:
        return { "message": str(e), "success": False}
    
print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
print(json.JSONEncoder().encode(handle_inquiry()))
