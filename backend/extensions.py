from flask_mail import Mail
from flask_socketio import SocketIO

mail = Mail()
email_controller = None
connected_users = {}

#socketio = SocketIO(cors_allowed_origins="*")
socketio = SocketIO(cors_allowed_origins="*", async_mode="gevent")