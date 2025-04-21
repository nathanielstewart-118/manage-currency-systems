import asyncio
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from pathlib import Path
from ..shared.utils import gen_sun, get_content, gen_barcode
from ..websocket_server.handler import send_to_all

current_file = Path(__file__)
load_dotenv()

def handle_get(handler, path):
    top = current_file.parent.parent.parent
    if path.find('index') > -1:
        view = top / "client/owners/index.html"
    elif path.find("supply-execution") > -1:
        view = top / "client/owners/supply-execution.html"

    content = get_content(view)
    handler.send_response(200)
    handler.send_header("Content-Type", "text/html")
    handler.end_headers()
    handler.wfile.write(content.encode())    
    
def handle_post(handler, form):
    command = form.get("command")
    print("This is post handler")
    result = ""
    if command == "supplier":
        result = handle_supplier_request(handler.server.db, form)
    elif command == "supply_open":
        result = handle_supply_open(handler.server.db, form)
    elif command == "supply_start":
        result = handle_supply_start(handler.server.db, form)
    elif command == "supply_end":
        result = handle_supply_end(handler.server.db, form)
    elif command == "supply_close":
        result = handle_supply_close(handler.server.db, form)
    elif command == "save_max_sales_amount":
        result = handle_save_max_amounts(handler.server.db, form)
        
    return result

def handle_supplier_request(db, form):
    try:
        owner_sun = form.get("owner_sun")
        cursor = db.cursor(dictionary=True)
        sql = f"select * from owners where owner_sun = '{owner_sun}'"
        cursor.execute(sql)
        owners = cursor.fetchall()
        if len(owners) == 0 or len(owners) > 1:
            data = {
                "success": False,
                "data": "Incorrect owner_sun"
            }
        else:
            owner = owners[0]
            sql = f"SELECT * FROM terminals WHERE JSON_CONTAINS('{owner["terminals"]}', JSON_QUOTE(terminals.tid))"
            cursor.execute(sql)
            terminals = cursor.fetchall()
            
            sql = f"SELECT * FROM restocks WHERE JSON_CONTAINS('{owner["terminals"]}', JSON_QUOTE(restocks.tid))"
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
    owner_sun = form.get("owner_sun")
    target_tid = form.get("target_tid")
    onetime_sun = gen_sun(3, "")
    cursor = db.cursor(dictionary=True)
    sql = f"INSERT INTO onetime_suns(onetime_sun, tid, owner_sun, created_at, updated_at) VALUES('{onetime_sun}', '{target_tid}', '{owner_sun}', '{datetime.now()}', '{datetime.now()}')"
    cursor.execute(sql)
    db.commit()    
    sql = f"SELECT * FROM restocks WHERE tid = '{target_tid}'"
    cursor.execute(sql)
    restocks = cursor.fetchall()
    sql = f"SELECT * FROM terminals WHERE tid = '{target_tid}'"
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

def handle_supply_start(db, form):
    onetime_sun = form.get("onetime_sun")
    tid = form.get("tid")
    cursor = db.cursor(dictionary=True)
    sql = f"select * from onetime_suns where onetime_sun = '{onetime_sun}' and tid = '{tid}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    return { "success": True } if len(results) == 0 else { "success": False }
    
    
def handle_supply_end(db, form):
    onetime_sun = form.get("onetime_sun")
    tid = form.get("tid")
    current_weight = form.get("gram")
    cursor = db.cursor(dictionary=True)
    sql = f"SELECT current_weight, max_sales_amount,currency_id, tid FROM restocks WHERE tid = '{tid}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    tid = form.get("tid")
    sql = "SELECT * FROM currencies"
    cursor.execute(sql)
    currencies = cursor.fetchall()
    data = json.dumps({
        "command": "supply_end",
        "currencies": currencies,   
        "grams": current_weight,
        "onetime_sun": onetime_sun,
        "tid": tid,
        "restocks": results
    }, default=str)    
    asyncio.run(send_to_all(data))
    return {
        "success": True,
        "message": "Supply end processed successfully"
    }

def handle_supply_close(db, form):
    try:
        onetime_sun = form.get("onetime_sun") or ""
        tid = form.get("tid") or ""
        cursor = db.cursor(dictionary=True)
        sql = f"DELETE FROM onetime_suns WHERE onetime_sun = '{onetime_sun}'"
        cursor.execute(sql)
        db.commit()
        msg = json.dumps({
            "command": "supply_close",
            "onetime_sun": onetime_sun,
            "tid": tid,
        })
        
        asyncio.run(send_to_all(msg))
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
        tid = form.get("tid")
        current_weight = form.get('current_weight')
        max_amounts = form.get("currency_amounts")
        cursor = db.cursor(dictionary=True)
        for amount in max_amounts:
            currency_id = amount.get("currency_id")
            max_sales_amount = amount.get("max_sales_amount")
            sql = f"SELECT * FROM restocks WHERE currency_id = {currency_id} AND tid = '{tid}'"
            cursor.execute(sql)
            records = cursor.fetchall()
            if len(records) == 1:
                sql = f"UPDATE restocks SET max_sales_amount = {max_sales_amount}, current_weight = {current_weight}, updated_at = '{datetime.now()}' WHERE currency_id = {currency_id} and tid = '{tid}'"
                cursor.execute(sql)
                db.commit()
            elif len(records) == 0:
                sql = f"INSERT INTO restocks(tid, currency_id, current_weight, max_sales_amount, created_at, updated_at) VALUES('{tid}', {currency_id}, {current_weight}, {max_sales_amount}, '{datetime.now()}', '{datetime.now()}')"
                cursor.execute(sql)
                db.commit()
            else:
                data = {
                    "success": False,
                    "data": "Several Records Already Exist"
                }
    except Exception as e:
        print(e)
        data = { "success": False, "data": str(e) }
    return data    

