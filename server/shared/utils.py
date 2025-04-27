import json 
import random
import barcode
from barcode.codex import Code39 
from barcode.writer import ImageWriter
from io import BytesIO
import base64
from string import Template

def authorize_terminal(tid, token, handler):
    cursor = handler.server.db.cursor(dictionary=True)
    sql = f"select * from terminals where tid = '{tid}'"
    cursor.execute(sql)
    terminals = cursor.fetchall()
    if tid is None or token is None:
        data = {
            "success": False,
            "error_code": "invalid auth data"
        }
        send_base(handler)
        handler.wfile.write(json.dumps(data).encode())
        return False
    elif len(terminals) == 1:
        
        if terminals[0]["token"] != token:
            data = {
                "success": False,
                "error_code": "invalid_token"
            }
            send_base(handler)
            handler.wfile.write(json.dumps(data).encode())
            return False
        else:
            return True
    else:
        data = {
            "success": False,
            "error_code": "Duplicate terminal or not exist"
        }
        send_base(handler)
        handler.wfile.write(json.dumps(data).encode())
        return False

def send_base(handler):
    handler.send_response(200)
    handler.send_header("Content-type", "application/json")
    handler.end_headers()

def get_content(path):
    with open(path, "r") as f:
        content = (f.read())
    # Render template with variables
    return content


def gen_sun(type, cur_sys_id):
    if type == 1:
        return f"2{cur_sys_id}{gen_random_digits(6)}"
    elif type == 2:
        return f"00{gen_random_digits(6)}"
    elif type == 3:
        return f"10{gen_random_digits(6)}"
    
def gen_random_digits(number):
   return str(random.randint(10**(number - 1), 10 ** number - 1)) 

def gen_barcode(data):
    barcode_image = Code39(data, writer=ImageWriter())
    print("this is after barcode init",data)
    buffer = BytesIO()
    barcode_image.write(buffer)
    # barcode_class(data, writer=ImageWriter()).write(buffer)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def send_response(handler, status_code, content_type, data):
    handler.send_response(status_code)
    handler.send_header("Content-type",content_type)
    handler.end_headers()
    handler.wfile.write(data)