#!./venv/bin/python3
#coding: utf-8

import os
import cgi
import json
import sys

from datetime import datetime
from dotenv import load_dotenv
import mysql.connector
from utils import gen_sun, gen_barcode
from logger import logger

load_dotenv()

def handle_supplier_request(db, form):
    try:
        owner_sun = form["owner_sun"].value
        cursor = db.cursor(dictionary=True)
        sql = f"select * from owners where owner_sun = '{owner_sun}'"
        cursor.execute(sql)
        owners = cursor.fetchall()
        if len(owners) != 1:
            data = {
                "success": False,
                "data": "Incorrect owner_sun"
            }
        else:
            owner = owners[0]
            sql = sql = f"""SELECT tid, area, product_name, key_string, token FROM terminals WHERE JSON_CONTAINS('{owner.get("terminals")}', JSON_QUOTE(terminals.tid))"""
            cursor.execute(sql)
            terminals = cursor.fetchall()
            sql = f"""SELECT tid, current_weight, currency_id, max_sales_amount FROM restocks WHERE JSON_CONTAINS('{owner.get("terminals")}', JSON_QUOTE(restocks.tid))"""
            cursor.execute(sql)
            restocks = cursor.fetchall()
            data = {
                "success": True,
                "data": {
                    "terminals": terminals,
                    "restocks": restocks
                }
            }
    except Exception as e:
        data = {
            "success": False,
            "data": str(e)
        }
    return data

def handle_supply_open(db, form):
    try:
        owner_sun = form.getfirst("owner_sun", "").strip()
        target_tid = form.getfirst("target_tid", "").strip()
        onetime_sun = gen_sun(3, "")
        cursor = db.cursor(dictionary=True)
        sql = f"INSERT INTO onetime_suns(onetime_sun, tid, owner_sun, created_at, updated_at) VALUES('{onetime_sun}', '{target_tid}', '{owner_sun}', '{datetime.now()}', '{datetime.now()}')"
        cursor.execute(sql)
        db.commit()
        sql = f"SELECT tid, current_weight, currency_id, max_sales_amount FROM restocks WHERE tid = '{target_tid}'"
        cursor.execute(sql)
        restocks = cursor.fetchall()
        sql = f"SELECT tid, area, product_name, key_string, token FROM terminals WHERE tid = '{target_tid}'"
        cursor.execute(sql)
        terminals = cursor.fetchall()
        terminal = terminals[0] if len(terminals) == 1 else {}

        return {
            "success": True,
            "data": {
                "restocks": restocks,
                "onetime_sun": onetime_sun,
                "barcode": gen_barcode(onetime_sun),
                "terminal": terminal                
            }
        }
    except Exception as e:
        return {
            "success": False,
            "data": str(e)
        }

def handle_supply_start(db, form):
    try:
        
        onetime_sun = form["onetime_sun"].value
        tid = form["tid"].value
        cursor = db.cursor(dictionary=True)
        sql = "SELECT * FROM currencies"
        cursor.execute(sql)
        currencies = cursor.fetchall()
        for cur in currencies:
            sql = f"SELECT * FROM restocks WHERE currency_id = {cur["id"]} and tid='{tid}'"
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) > 0:
                continue
            sql = f"INSERT INTO restocks(tid, current_weight, currency_id, max_sales_amount, created_at, updated_at) VALUES('{tid}', 0, {cur["id"]}, 0, '{datetime.now()}', '{datetime.now()}')"
            cursor.execute(sql)
            db.commit()
        sql = f"select * from onetime_suns where onetime_sun = '{onetime_sun}' and tid = '{tid}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        return { "success": True } if len(results) == 1 else { "success": False }
    except Exception as e:
        return {
            "success": False,
            "data": str(e)
        }
    
def handle_supply_end(db, form):
    try:
        tid = form["tid"].value
        current_weight = form["gram"].value
        cursor = db.cursor(dictionary=True)
        sql = f"UPDATE restocks SET current_weight={current_weight} WHERE tid = '{tid}'"
        cursor.execute(sql)
        db.commit()
        return {
            "success": True,
            "message": "Supply end processed successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

def handle_supply_close(db, form):
    try:
        onetime_sun = form["onetime_sun"].value or ""
        tid = form["tid"].value or ""
        cursor = db.cursor(dictionary=True)
        sql = f"DELETE FROM onetime_suns WHERE onetime_sun = '{onetime_sun}'"
        cursor.execute(sql)
        db.commit()
        msg = json.dumps({
            "command": "supply_close",
            "onetime_sun": onetime_sun,
            "tid": tid,
        })
        
    except Exception as e:
        print(e)
        return {
            "success": False,
            "data": str(e)
        }
    
    return {
        "success": True,
        "message": "Supply closed successfully."
    }
    
def handle_save_max_amounts(db, form):
    data = { "success": True }
    try:
        return data
        target_tid = form["target_tid"].value
        current_weight = form['current_weight'].value
        max_amounts = form["currency_amounts"].value
        cursor = db.cursor(dictionary=True)
        for amount in max_amounts:
            currency_id = amount.get("currency_id")
            max_sales_amount = amount.get("max_sales_amount")
            sql = f"SELECT * FROM restocks WHERE currency_id = {currency_id} AND tid = '{target_tid}'"
            cursor.execute(sql)
            records = cursor.fetchall()
            if len(records) == 1:
                sql = f"UPDATE restocks SET max_sales_amount = {max_sales_amount}, current_weight = {current_weight}, updated_at = '{datetime.now()}' WHERE currency_id = {currency_id} and tid = '{target_tid}'"
                cursor.execute(sql)
                db.commit()
            elif len(records) == 0:
                sql = f"INSERT INTO restocks(tid, currency_id, current_weight, max_sales_amount, created_at, updated_at) VALUES('{target_tid}', {currency_id}, {current_weight}, {max_sales_amount}, '{datetime.now()}', '{datetime.now()}')"
                cursor.execute(sql)
                db.commit()
            else:
                data = {
                    "success": False,
                    "data": "Several Records Already Exist"
                }
    except Exception as e:
        data = { "success": False, "data": str(e) }
    return data    

def handle_get_restock(db, form):
    try:
        onetime_sun = form["onetime_sun"].value
        target_tid = form["target_tid"].value
        cursor = db.cursor(dictionary=True)
        sql = f"SELECT current_weight, max_sales_amount,currency_id, tid FROM restocks WHERE tid = '{target_tid}'"
        cursor.execute(sql)
        restocks = cursor.fetchall()
        sql = "SELECT * FROM currencies"
        cursor.execute(sql)
        currencies = cursor.fetchall()
        
        current_weight = restocks[0]["current_weight"] if len(restocks) > 0 else 0
        return {
            "success": True,
            "data": {
                "currencies": currencies,   
                "grams": current_weight,
                "onetime_sun": onetime_sun,
                "tid": target_tid,
                "restocks": restocks
            }   
        }
    except Exception as e:
        return {
            "success": False,
            "data": str(e)
        }    

result, db = None, None    
try:
    db = mysql.connector.connect(
        host=os.getenv("DB_URL"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        auth_plugin="mysql_native_password"
    )
    form = cgi.FieldStorage()
    log_id = logger.log_request(form)
    command = form.getfirst("command", "").strip()
    if command == "supplier":
        result = handle_supplier_request(db, form)
    elif command == "supply_open":
        result = handle_supply_open(db, form)
    elif command == "supply_start":
        result = handle_supply_start(db, form)
    elif command == "supply_end":
        result = handle_supply_end(db, form)
    elif command == "supply_close":
        result = handle_supply_close(db, form)
    elif command == "save_max_sales_amount":
        result = handle_save_max_amounts(db, form)
    elif command == "get_restock":
        result = handle_get_restock(db, form)
    else:
        result = { "success": False, "data": "invalid command" }

    logger.log_response(log_id, result)
except Exception as e:
    result = str(e)
finally:
    if db:
        db.close()
    print ("Access-Control-Allow-Headers: Origin, Content-Type\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS\r\nContent-Type: application/json\r\n")
    print(json.dumps(result, default=str))