from models.notification import Notification
from database import db
from datetime import datetime

def create_notification(user_id=None, message="", is_global=False):
    try:
        notification = Notification(
            user_id=user_id,
            message=message,
            is_read=False,
            created_at=datetime.utcnow(),
            is_global=is_global
        )
        db.session.add(notification)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao salvar notificação: {e}")
        db.session.rollback()

def get_unread_notifications(user_id):
    notifications = Notification.query.filter(
        ((Notification.user_id == user_id) | (Notification.is_global == True)) &
        (Notification.is_read == False)
    ).order_by(Notification.created_at.desc()).all()

    return [
        {
            'id': n.id,
            'message': n.message,
            'created_at': n.created_at
        } for n in notifications
    ]

def mark_notification_as_read(notification_id):
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_read = True
        db.session.commit()
