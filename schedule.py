import schedule
import time

def job():
    print("iso")

def job2():
    print("2")

schedule.every(10).minutes.do(job)

schedule.every(2).seconds.do(job)
schedule.every(1).seconds.do(job2)

while 1:
    schedule.run_pending()
    time.sleep(1)