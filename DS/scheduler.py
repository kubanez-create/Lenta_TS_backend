from apscheduler.schedulers.background import BackgroundScheduler

from app import main

scheduler = BackgroundScheduler()
scheduler.add_job(main, 'interval', days=1)

try:
    scheduler.start()
except KeyboardInterrupt:
    scheduler.shutdown()
