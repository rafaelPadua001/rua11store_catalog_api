from flask_mail import Mail
from flask_socketio import SocketIO

mail = Mail()
email_controller = None 

socketio = SocketIO(cors_allowed_origins="*")