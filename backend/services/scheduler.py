from apscheduler.schedulers.background import BackgroundScheduler
from services.recovery_service import RecoveryService
from app import app

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=run_with_app_context(), trigger="interval", minutes=30)
    scheduler.start()

def run_with_app_context():
    with app.app_context():
        RecoveryService.check_and_send_recovery_emails(hours=1)