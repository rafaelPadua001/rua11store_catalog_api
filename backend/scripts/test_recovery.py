import os
import sys
from dotenv import load_dotenv

# Garante que o projeto inteiro está no path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carrega o .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

from app import app
from services.recovery_service import RecoveryService

with app.app_context():
    RecoveryService.check_and_send_recovery_emails(hours=1)
