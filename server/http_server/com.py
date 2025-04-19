import json
import secrets
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
from ..shared.state import State
from ..shared.utils import gen_sun
load_dotenv()

delay_hour = float(os.getenv("DELAY_HOUR"))

def handle(form, handler):

    command = form.get("command")
    handler.send_response(200)
    handler.send_header("Content-type", "application/json")
    handler.end_headers()
    if command == "init":
        return init(form, handler)
    elif command == "req_token":
        return req_token(form, handler)
    elif command == 'req_sun':
        return req_sun(form, handler)
    elif command == 'req_config':
        return req_config(form, handler)
    elif command == 'service_in':
        return service_in(form, handler)
    elif command == 'service_out':
        return service_out(form, handler)
    elif command == 'service_togo':
        return service_togo(form, handler)
    elif command == 'refresh_db':
        return refresh_db(handler.server.db)
    elif command == 'life_signal':
        return life_signal(handler, form, handler.server.db)
    
def init(form, handler):
    try:
        data = {
            "success": True,
        }
        tid = form.get('tid')
        token = form.get('token')
        print(tid, token)
        cursor = handler.server.db.cursor(dictionary=True)
        
        sql = f"select * from terminals where tid='{tid}'"
        cursor.execute(sql)
        terminals = cursor.fetchall()
        
        if len(terminals) == 0:
            data = {
                "success": False,
                "data": "no matching terminal"
            }
        elif len(terminals) > 1:
            data = {
                "success": False,
                "data": "duplicated terminals"
            } 
        elif terminals[0].get("token") != token:
                data = {
                    "success": False,
                    "data": "token mismatch"
                }
        else:
            sql = f"select prices.currency_id, terminals.amount * prices.price as max_sales_amount from terminals inner join prices on ( terminals.product_id = prices.product_id) where tid='{tid}'"
            cursor.execute(sql)
            total_values = cursor.fetchall()
            
            sql = "select * from currencies" 
            cursor.execute(sql)
            currencies = cursor.fetchall()
            
            sql = """
            SELECT o.*, a.cur_sys_id, a.uid
            FROM owners o
            JOIN accounts a
            ON JSON_CONTAINS(o.accounts, JSON_QUOTE(CAST(a.id AS CHAR))) WHERE JSON_CONTAINS(terminals, %s)
            """
            cursor.execute(sql, (json.dumps(tid),))
            owners = cursor.fetchall()
            
            if len(owners) > 0:
                owner = {
                    "owner_name": owners[0]["owner_name"],
                    "owner_sun": owners[0]["owner_sun"],
                    "accounts": [],
                    "terminals": owners[0]["terminals"]
                }
                accounts = []
                for a in owners:
                    accounts.append({
                        "cur_sys_id": a["cur_sys_id"],
                        "uid": a["uid"]
                    })
                owner["accounts"] = accounts
            else:
                owner = {}
            data["data"] = {
                "total_values": total_values,
                "currencies": currencies,
                "owner": owner 
            }
    except Exception as e:
        data = {
            "success": False,
            "data": str(e)
        }
    return json.dumps(data).encode()
        
def req_token(form, handler):
    try:
        data = {
            "success": True,
            "data": {
                
            }
        }
        tid = form.get("tid")
        cursor = handler.server.db.cursor(dictionary=True)
        sql = f"SELECT * FROM terminals where tid = '{tid}'"
        cursor.execute(sql)
        records = cursor.fetchall()
        if len(records) == 0:
            data["data"] = "no terminal with that id"
        elif len(records) == 1:
            key = form.get("key")
            if key == records[0].get("key"):
                token = secrets.token_hex(16)
                data["data"] = token
            else:
                data["success"] = False
                data["data"] = "The key field doesn't match!"
        else:
            data["success"] = False
            data["data"] = "duplicated terminal id"
        print(type(records), records)
        data["data"] = records
        
    except Exception as e:
        data["success"] = False
        data["data"] = str(e)
    return json.dumps(data, default=str)
        

def req_config(form, handler):
    try:
        data = {
            "success": True,
            "data": {
                "mains": "https://www.48v.me/~mains",
                "controlSUNNumber": "99993",
                "ifservernoreaction": "",
                "servicetype": "",
                "serviceprice": "",
            }
        }
    except Exception as e:
        data["success"] = False
        data["data"] = str(e)
    return json.dumps(data, default=str)
        
def req_sun(form, handler):
    data = {
        "success": True,
    }
    try:
        cur_sys_id = form.get("CurSysID")
        uid = form.get("uid")
        tid = form.get("tid")
        db = handler.server.db
        cursor = db.cursor(dictionary=True)
        sql = f"select * from suns where cur_sys_id = '{cur_sys_id}' and uid = '{uid}' and tid = '{tid}'"
        cursor.execute(sql)
        suns = cursor.fetchall()
        if len(suns) == 0:
            new_sun = gen_sun(1, cur_sys_id)
            data = {
                "success": True,
                "sun": new_sun,
                "message": "new",
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            sql = f"insert into suns(cur_sys_id, uid, tid, sun, created_at, updated_at) values({cur_sys_id}, '{uid}', '{tid}', '{new_sun}', '{datetime.now()}', '{datetime.now()}')"
        else:
            sun = suns[-1]
            diff_hours = (datetime.now() - sun.get("updated_at")).total_seconds() / 3600
            if diff_hours < delay_hour:
                data = {
                    "success": True,
                    "sun": sun["sun"],
                    "message": "registered",
                    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                sql = f"Update suns set updated_at = '{datetime.now()}' where id = {sun["id"]}"
            else:
                new_sun = gen_sun(1, cur_sys_id)
                data = {
                    "success": True,
                    "sun": new_sun,
                    "message": "new",
                    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                sql = f"insert into suns(cur_sys_id, uid, tid, sun, created_at, updated_at) values({cur_sys_id}, '{uid}', '{tid}', '{new_sun}', '{datetime.now()}', '{datetime.now()}')"
            cursor.execute(sql)
            db.commit()        
            
    except Exception as e:
        data["success"] = False
        data["data"] = str(e)
    return json.dumps(data, default=str)
        
def service_in(form, handler):
    data = {
        "success": True,
    }
    state = State()
    
    try:
        sun = form.get("sun")
        db = handler.server.db
        cursor = db.cursor(dictionary=True)
        sql = f"select * from suns where sun = '{sun}'"
        cursor.execute(sql)
        suns = cursor.fetchall()
        if len(suns) == 0:
            data = {
                "success": False,
                "error_code": "USER_NOT_FOUND"
            }
        else:
            sun = suns[-1]
            if (datetime.now() - sun.get("updated_at")).total_seconds() / 3600 < delay_hour:
                if state.service_semaphore:
                    data = {
                        "success": False,
                        "error_code": "INUSE"
                    }
                else:
                    sql = f"update suns set updated_at = '{datetime.now()}' where id={sun["id"]}"
                    cursor.execute(sql)
                    db.commit()
                    state.service_semaphore = True
                    data = {
                        "success": True,
                        "uid": sun["uid"],
                        "curSysID": sun["cur_sys_id"]
                    }
            else:
                data = {
                    "success": False,
                    "error_code": "USER_NOT_FOUND"
                }
                
        
    except Exception as e:
        data["success"] = False
        data["data"] = str(e)
    return json.dumps(data, default=str)
        
def service_out(form, handler):
    data = {
        "success": True,
    }
    try:
        sun = form.get("sun")
        gram = form.get("gram")
        max_sales_amount = form.get("max_sales_amount")
        db = handler.server.db
        cursor = db.cursor(dictionary=True)
        sql = f"select * from suns where sun = '{sun}'"
        cursor.execute(sql)
        suns = cursor.fetchall()
        if len(suns) == 0:
            data = {
                "success": False,
                "error_code": "INVALID_REQUEST"
            }
        else:
            sun = suns[-1]
            if (datetime.now() - sun.get("updated_at")).total_seconds() / 3600 < delay_hour:
                # update the total value
                
                
                sql = f"update suns set updated_at = '{datetime.now()}', gram = {gram}, max_sales_amount = {max_sales_amount} where id = {sun["id"]}"
                cursor.execute(sql)
                db.commit()
                state = State()
                if state.service_semaphore:
                    state.service_semaphore = False
                    data = {
                        "success": True
                    }
            else:
                data = {
                    "success": False,
                    "data": "Time exceeds from the last access"
                }
    except Exception as e:
        data["success"] = False
        data["data"] = str(e)
    return json.dumps(data, str)
        
def service_togo(form, handler):
    data = {
        "success": True,
    }
    try:
        sun = form.get("sun")
        gram = form.get("gram")
        max_sales_amount = form.get("max_sales_amount")
        db = handler.server.db
        cursor = db.cursor(dictionary=True)
        sql = f"select * from suns where sun = '{sun}'"
        cursor.execute(sql)
        suns = cursor.fetchall()
        if len(suns) == 0:
            data = {
                "success": False,
                "error_code": "INVALID_REQUEST"
            }
        else:
            sun = suns[-1]
            if (datetime.now() - sun.get("updated_at")).total_seconds() / 3600 < delay_hour:
                state = State()
                if state.service_togo_semaphore:
                    data = {
                        "success": False,
                        "error_code": "INUSE"
                    }
                else:
                    # update total value with currency_id and max_sales_amount
                    sql = f"update suns set updated_at = '{datetime.now()}', gram = {gram}, max_sales_amount = {max_sales_amount} where id = {sun["id"]}"
                    cursor.execute(sql)
                    db.commit()
                    state = State()
                    if state.service_togo_semaphore:
                        state.service_togo_semaphore = False
                        data = {
                            "success": True
                        }
            else:
                data = {
                    "success": False,
                    "data": "time exceeds from the last access"
                }
    except Exception as e:
        data["success"] = False
        data["data"] = str(e)
    return json.dumps(data, default=str)
        
def refresh_db(db):
    try:
        cursor = db.cursor(dictionary = True)
        sql = f"DELETE * FROM suns WHERE updated_at <= DATE_SUB(NOW(), INTERVAL, {os.getenv("REFRESH_MONTH")} MONTH)"
        cursor.execute(sql)
        db.commit()
        
        sql = f"DELETE * FROM onetime_suns WHERE updated_at <= DATE_SUB(NOW(), INTERVAL, {os.getenv("REFRESH_MONTH")} MONTH)"
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        return { "success": False }
    return { "success": True }

        
def life_signal(handler, form, db):
    try:
        cursor = db.cursor(dictionary=True)
        ip_address = handler.client_address[0] or ""
        tid = form.get("tid") or ""
        sql = f"INSERT into logs(ip_address, tid, command, received_json, sent_json, created_at, updated_at) VALUES('{ip_address}', '{tid}', 'life_signal', '{json.dumps(form)}', '{datetime.now()}', '{datetime.now()}')"
        cursor.execute(sql)
        db.commit()
        return { "success": True }
    except Exception as e:
        print(e)
        return { "success": False, "message": str(e) }


