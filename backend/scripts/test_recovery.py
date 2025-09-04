import os
import sys
from dotenv import load_dotenv

# Adiciona a pasta 'backend' ao path para o Python achar o app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carrega variáveis do .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# Agora o Python consegue importar app.py
from app import app
from services.recovery_service import RecoveryService

if __name__ == "__main__":
    RecoveryService.check_and_send_recovery_emails(app, hours=1)
