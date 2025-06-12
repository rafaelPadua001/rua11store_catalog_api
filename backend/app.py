from gevent import monkey
monkey.patch_all()
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import Config
from database import db
from routes import register_routes
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from controllers.emailController import EmailController
from extensions import socketio, mail, email_controller  # ← pegar de extensions
from routes.notification import notification_bp, register_socketio_events
from flask_sqlalchemy import SQLAlchemy
import socket
import re

load_dotenv()
app = Flask(__name__, static_folder="uploads", static_url_path="/uploads")
app.config.from_object(Config)
raw_db_url = os.getenv("DATABASE_URL")

if raw_db_url.startswith("postgresql://"):
    raw_db_url = raw_db_url.replace("postgresql://", "postgresql+psycopg2://")

    match = re.match(r"(postgresql\+psycopg2://[^@:]+:[^@]+@)([^:/]+)(:\d+/.+)", raw_db_url)
    if match:
        prefix, host, suffix = match.groups()
        try:
            ipv4 = socket.gethostbyname(host)
            raw_db_url = f"{prefix}{ipv4}{suffix}"
            print(f"Conectando ao banco via IPv4: {ipv4}")
        except socket.gaierror:
            print(f"Não foi possível resolver o host {host} para IPv4, mantendo o original.")

# ATENÇÃO: aqui a variável raw_db_url já está modificada ou não, mas nunca será None
app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


CORS(app, resources={r"/*": {"origins": "*"}})

bcrypt = Bcrypt(app)

app.config["JWT_SECRET_KEY"] = "headers"     
jwt = JWTManager(app)

# Banco de dados
db.init_app(app)
with app.app_context():
    db.create_all()

# Rotas
register_routes(app)

# SocketIO

socketio.init_app(app)
register_socketio_events(socketio)

# E-mail

app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS') == 'True',
    MAIL_USERNAME=os.getenv('GMAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('GMAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
)
mail.init_app(app)  # ← inicializar a instância já importada
email_ctrl = EmailController(mail)

# 🔁 Atualiza a instância no extensions (forma correta)
import extensions
extensions.email_controller = email_ctrl

# Executar servidor
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
