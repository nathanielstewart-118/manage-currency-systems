#!./.venv/bin/python
#coding: utf-8

import os
import json
# import cgi

# Open the log file in read mode


# # Print the logs to verify
# for log in logs:
#     print(f"MID: {log['mid']}, Area: {log['area']}, Action: {log['action']}, Date: {log['date']}")
def logs_data():
    with open("logs/logs.json", "r") as file:
        logs = json.load(file)
    return {"logs": logs}

print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
print(json.JSONEncoder().encode(logs_data()))