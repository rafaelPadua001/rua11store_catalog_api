from flask import Blueprint, request, jsonify
from flask_socketio import emit, join_room, leave_room
from utils.notifications_utils import create_notification, get_unread_notifications, mark_notification_as_read
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from services.fcm_service import send_fcm_notification
import logging

logger = logging.getLogger(__name__)

notification_bp = Blueprint('notifications', __name__)
connected_users = {}
socketio = None  # variável global para usar socketio

def register_socketio_events(sio):
    global socketio
    socketio = sio  # guarda a instância do socketio para usar nas rotas

    @socketio.on('connect')
    def handle_connect():
       # user_id = request.args.get('user_id')

        print("SOCKET CONNECTED sid=", request.sid)

        #if user_id:
      #      connected_users[user_id] = request.sid
       #     print(f"USER CONNECTED: {user_id} -> {request.sid}")
        
        logger.info(f"SOCKET CONNECTED sid={request.sid}")

    @socketio.on('auth')
    def handle_auth(data):
        user_id = str(data.get('user_id'))
        join_room(str(user_id))
        print("Usuário entrou na sala:", user_id)
        if not user_id:
            print("AUTH sem user_id — ignorado")
            return

        connected_users[user_id] = request.sid
        print(f"AUTH OK — user_id={user_id} sid={request.sid}")

    @socketio.on('disconnect')
    def handle_disconnect():
        print("DISCONNECT sid=", request.sid)
        for user_id, sid in list(connected_users.items()):
            if sid == request.sid:
                del connected_users[user_id]
                print(f"Removed {user_id} from connected_users")
                break

@notification_bp.route('/notifications/<string:user_id>', methods=['GET', 'OPTIONS'])
def get_notifications(user_id):
    if request.method == 'OPTIONS':
        return '', 204

    verify_jwt_in_request()
    token_user_id = get_jwt_identity()

    print(f"token_user_id={token_user_id} (type={type(token_user_id)}), user_id={user_id} (type={type(user_id)})")

    if token_user_id != str(user_id):
        print("Unauthorized access attempt")
        return jsonify({"error": "Unauthorized"}), 403


    print("Authorized!")
    notifications = get_unread_notifications(user_id)
    return jsonify(notifications)


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
        socketio.emit(f'notification_global', {'message': message})

    return jsonify({'status': 'sent'})

@notification_bp.route('/send-notification', methods=['POST'])
def send_notification():
    data = request.json
    token = data.get('token')
    title = data.get('title', 'Nova Notificação')
    body = data.get('body', '')
    link = data.get('link', 'https://rua11store-web.vercel.app/')

    if not token:
        return jsonify({"error": "Token não informado"}), 400
    
    resp = send_fcm_notification(token, title, body, link)
    return jsonify({"status": resp.status_code, "response": resp.json})




