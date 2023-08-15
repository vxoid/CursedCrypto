from import_bot import *
from texts import *
import schedule

def notify():
  schedule.every(10).seconds.do(check_for_new_entries)

  while True:
    schedule.run_pending()
    time.sleep(1)

def check_for_new_entries():
  pass