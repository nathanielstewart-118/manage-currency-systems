#!./.venv/bin/python
#coding: utf-8

import random
import os
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
def get_config_list():
    try:
        mycursor = mydb.cursor(dictionary=True)
        form = cgi.FieldStorage()
        area = form["area"].value
        if (area == "all"):
            sql = "SELECT * FROM terminals"
        else:
            sql = "SELECT * FROM terminals where service_area = '" + area + "'"
        mycursor.execute(sql)
        sun_data = mycursor.fetchall()
        for entry in sun_data:
            for key, value in entry.items():
                if isinstance(value, datetime):  # Use 'datetime' without 'datetime.datetime'
                    entry[key] = value.isoformat()
        return {"config_files": sun_data}
    except Exception as e:
        return { "message": str(e), "success": False}
    
print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
print(json.JSONEncoder().encode(get_config_list()))