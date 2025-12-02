#from gevent import monkey
#monkey.patch_all()

from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

from config import Config
from database import db
from routes import register_routes
from controllers.emailController import EmailController
from extensions import socketio, mail, email_controller
from routes.notification import notification_bp, register_socketio_events
from apscheduler.schedulers.background import BackgroundScheduler
from services.recovery_service import RecoveryService
from dotenv import load_dotenv

import os
import socket
import re
import cloudinary
import cloudinary.uploader



# Carrega variáveis do .env
load_dotenv()

# Cria app
app = Flask(__name__, static_folder="uploads", static_url_path="/uploads")
app.config.from_object(Config)

# 👉 Trata DATABASE_URL para forçar IPv4
# Apenas isso: mantemos a URL original do Supabase
raw_db_url = os.getenv("DATABASE_URL", "")
# if raw_db_url.startswith("postgresql://"):
#     raw_db_url = raw_db_url.replace("postgresql://", "postgresql+psycopg2://")

# Sem usar socket.gethostbyname()
app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_url


# Configura SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Bcrypt
bcrypt = Bcrypt(app)

# JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "headers")  # Mais seguro via .env
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 900))
)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
    seconds=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 2592000))
)

jwt = JWTManager(app)

# Banco de dados
db.init_app(app)
with app.app_context():
    db.create_all()

# Rotas
register_routes(app)

# SocketIO
socketio.init_app(app, cors_allowed_origins="*", async_mode="eventlet")
register_socketio_events(socketio)

# E-mail
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'True') == 'True',
    MAIL_USERNAME=os.getenv('GMAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('GMAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
)
mail.init_app(app)



email_ctrl = EmailController(mail)
import extensions
extensions.email_controller = email_ctrl

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=RecoveryService.check_and_send_recovery_emails,
    trigger="interval",
    minutes=15,
    args=[app],
    kwargs={"hours": 1}
)

scheduler.start()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Rodar servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
