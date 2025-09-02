from apscheduler.schedulers.background import BackgroundScheduler
from services.recovery_service import check_and_send_recovery_emails

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_and_send_recovery_emails, trigger="interval", minutes=30)
    scheduler.start()
