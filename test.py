import schedule
import time

def job():
    print("Running job...")

schedule.every(10).seconds.do(job)
# schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
