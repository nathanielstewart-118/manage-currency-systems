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
        
def handle_new_min_sun():
    try:
        # Read form data
        form = cgi.FieldStorage()
        area = form["area"].value
        deposit = float(form.getfirst("deposit", "0"))
        sun_duration = 24

        mycursor = mydb.cursor(dictionary=True)

        # Generate MID
        today = datetime.now().strftime('%y%m%d')
        mycursor.execute(f"SELECT mid FROM mids WHERE mid LIKE '{today}%' ORDER BY mid DESC LIMIT 1")
        last_mid = mycursor.fetchone()

        if last_mid:
            last_serial = int(last_mid['mid'][-3:])
            new_serial = last_serial + 1
        else:
            new_serial = 1

        mid = f"{today}{new_serial:03}"
        mid_expire_date = datetime.now() + timedelta(days=180)

        # Insert MID
        sql = "INSERT INTO mids (mid, issue_date, deposit, expire_date) VALUES (%s, NOW(), %s, %s)"
        mycursor.execute(sql, (mid, deposit, mid_expire_date))

        # Check for existing SUN
        sql = f"SELECT * FROM suns WHERE mid = '{mid}' AND expire_date > NOW()"
        mycursor.execute(sql)
        existing_sun = mycursor.fetchone()

        if existing_sun:
            sun = existing_sun['sun']
            sun_expire_date = existing_sun['expire_date']
        else:
            # Clean expired SUNs
            sql = f"DELETE FROM suns WHERE mid = '{mid}' AND expire_date < NOW()"
            mycursor.execute(sql)
            sun = f"{random.randint(10**7, 10**8 - 1)}"
            sun_expire_date = datetime.now() + timedelta(hours=sun_duration)

            # Insert new SUN
            sql = "INSERT INTO suns (mid, sun, expire_date) VALUES (%s, %s, %s)"
            mycursor.execute(sql, (mid, sun, sun_expire_date))
        
        mydb.commit()

        log_write(mid, area, "new MID and SUN create and deposit: " + str(deposit))
    
        return {
            "message": "MID and SUN generated",
            "MID": mid,
            "SUN": sun,
            "MID_expire_date": mid_expire_date.strftime('%Y-%m-%d %H:%M:%S'),
            "SUN_expire_date": sun_expire_date.strftime('%Y-%m-%d %H:%M:%S'),
            "success": True
        }

    except Exception as e:
        return {"message": str(e), "success": False}

print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
print(json.dumps(handle_new_min_sun()))



