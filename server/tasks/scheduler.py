import schedule
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def check_suns(db):
    print(f"Running job...{os.getenv("DELAY_HOUR")}")
    try:
        cursor = db.cursor(dictionary=True)
        sql = f"UPDATE suns SET expired_at = '{datetime.now()}' WHERE updated_at < DATE_SUB(NOW(), INTERVAL {os.getenv("DELAY_HOUR")} HOUR) and expired_at IS null"
        cursor.execute(sql)
        db.commit()
        
        sql = f"UPDATE onetime_suns SET expired_at = '{datetime.now()}' WHERE updated_at < DATE_SUB(NOW(), INTERVAL {os.getenv("DELAY_HOUR")} HOUR) and expired_at IS null"
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)    

def start_scheduler(db):
    schedule.every(10).seconds.do(lambda: check_suns(db))
    while True:
        schedule.run_pending()
        time.sleep(1)
# schedule.every().day.at("10:30").do(job)

