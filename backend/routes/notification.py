from flask import Blueprint, request, jsonify
from flask_socketio import emit
from utils.notifications_utils import create_notification, get_unread_notifications, mark_notification_as_read

notification_bp = Blueprint('notifications', __name__)
connected_users = {}
socketio = None  # variável global para usar socketio

@notification_bp.route('/notifications/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    return jsonify(get_unread_notifications(user_id))

@notification_bp.route('/notifications/read/<int:notification_id>', methods=['POST'])
def read_notification(notification_id):
    mark_notification_as_read(notification_id)
    return jsonify({"status": "ok"})

@notification_bp.route('/notify', methods=['POST'])
def notify():
    global socketio
    data = request.json
    user_id = data['user_id']
    message = data['message']
    create_notification(user_id, message)

    if user_id in connected_users and socketio:
        socketio.emit(f'notification_{user_id}', {'message': message}, to=connected_users[user_id])

    return jsonify({'status': 'sent'})

def register_socketio_events(sio):
    global socketio
    socketio = sio  # guarda a instância do socketio para usar nas rotas

    @socketio.on('auth')
    def handle_auth(data):
        user_id = data.get('user_id')
        if user_id:
            connected_users[user_id] = request.sid

    @socketio.on('disconnect')
    def handle_disconnect():
        for user_id, sid in list(connected_users.items()):
            if sid == request.sid:
                del connected_users[user_id]
