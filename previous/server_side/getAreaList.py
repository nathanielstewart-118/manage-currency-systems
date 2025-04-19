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
def get_area_list():
    try:
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT DISTINCT service_area FROM terminals;"
        mycursor.execute(sql)
        sun_data = mycursor.fetchall()
        return {"config_files": sun_data}
    except Exception as e:
        return { "message": str(e), "success": False}
    
print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
print(json.JSONEncoder().encode(get_area_list()))