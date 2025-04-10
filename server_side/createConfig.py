#!./.venv/bin/python
#coding: utf-8

import random
import os
from datetime import datetime, timedelta
import cgi
import json
import mysql.connector
import uuid

mydb = mysql.connector.connect(
  host="localhost",
  user="minifooko_dev",
  password="uj9Qta3b#Via",
  database="minifooko_db_dev",
  auth_plugin="mysql_native_password"
)

def create_json_file():
    try:
        form = cgi.FieldStorage()
        id = form["id"].value
        area = form["area"].value
        
        serverURL = "https://48v.me/~minifooko/cgi-bin/"
        controlMIDnumber = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        controlSUNnumber = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        auth = str(uuid.uuid4())
        ifservernoreaction = "CONTINUE"
        servicetype = "COFFE_MACHINE"
        serviceprice = 30
        etc = "ANY"

        data = {
            "serverURL": serverURL, 
            "controlMIDnumber": controlMIDnumber, 
            "controlSUNnumber": controlSUNnumber, 
            "auth": auth, 
            "ifservernoreaction": ifservernoreaction, 
            "servicetype": servicetype, 
            "serviceprice": serviceprice, 
            "etc": etc
        }
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT * FROM terminals WHERE terminal_id = '" + id + "' and service_area = '" + area + "'"
        mycursor.execute(sql)
        sun_data = mycursor.fetchone()
        if sun_data:
            sdata = {
                "serverURL": sun_data['serverURL'], 
                "controlMIDnumber": sun_data['controlMIDnumber'], 
                "controlSUNnumber": sun_data['controlSUNnumber'], 
                "auth": sun_data['auth'], 
                "ifservernoreaction": sun_data['ifservernoreaction'], 
                "servicetype": sun_data['servicetype'], 
                "serviceprice": sun_data['serviceprice'], 
                "etc": sun_data['etc']
            }   
            return sdata
        else : 
            sql = "INSERT INTO terminals (terminal_id, service_area, serverURL, controlMIDnumber, controlSUNnumber, auth, ifservernoreaction, servicetype, serviceprice, etc, last_access) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"
            mycursor.execute(sql, (id, area, serverURL, controlMIDnumber, controlSUNnumber, auth, ifservernoreaction, servicetype, serviceprice, etc))
            mydb.commit()
            return data
    except Exception as e:
        return {"message": str(e), "success": False}

print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
print(json.JSONEncoder().encode(create_json_file()))
