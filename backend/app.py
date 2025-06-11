import eventlet
eventlet.monkey_patch()
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


load_dotenv()
app = Flask(__name__, static_folder="uploads", static_url_path="/uploads")
app.config.from_object(Config)
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
