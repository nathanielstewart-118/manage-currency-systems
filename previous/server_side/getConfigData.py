#!./.venv/bin/python
#coding: utf-8
from datetime import datetime, timedelta
import json
import cgi
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="minifooko_dev",
  password="uj9Qta3b#Via",
  database="minifooko_db_dev",
  auth_plugin="mysql_native_password"
)

def read_config_data():
    try:
        mycursor = mydb.cursor(dictionary=True)

        form = cgi.FieldStorage()
        id = form["id"].value  
        sql = "SELECT * FROM terminals WHERE id=" + id
        mycursor.execute(sql)
        terminal_data = mycursor.fetchall()
        for entry in terminal_data:
            for key, value in entry.items():
                if isinstance(value, datetime):  # Use 'datetime' without 'datetime.datetime'
                    entry[key] = value.isoformat()
        return {"terminal_data": terminal_data}
    
    except Exception as e:
        return { "message": str(e), "success": False}

print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
print(json.JSONEncoder().encode(read_config_data()))
