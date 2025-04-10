#!./.venv/bin/python
#coding: utf-8
from datetime import datetime, timedelta
import json
import cgi
import mysql.connector
import os, sys

mydb = mysql.connector.connect(
  host="localhost",
  user="minifooko_dev",
  password="uj9Qta3b#Via",
  database="minifooko_db_dev",
  auth_plugin="mysql_native_password"
)

def save_config_data():
    try:
        mycursor = mydb.cursor(dictionary=True)

        content_length = int(os.environ.get("CONTENT_LENGTH", 0))
        body = sys.stdin.read(content_length)
        data = json.loads(body)
        sql = "UPDATE terminals SET serverURL = %s, controlMIDnumber = %s, controlSUNnumber= %s,ifservernoreaction =%s, auth = %s, servicetype= %s, serviceprice=%s, etc=%s, last_access=NOW() where id="+data['id']
        
        mycursor.execute(sql, (data['serverURL'], data['controlMIDnumber'], data['controlSUNnumber'], data['ifservernoreaction'], data['auth'], data['servicetype'], data['serviceprice'], data['etc'] ))
        mydb.commit()
        return {"message": "success", "success": False}
    
    except Exception as e:
        return { "message": str(e), "success": False}

print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
print(json.JSONEncoder().encode(save_config_data()))
