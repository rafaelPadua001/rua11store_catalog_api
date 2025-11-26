from models.notification import Notification
from database import db
from datetime import datetime
class NotificationController:
    @staticmethod
    def create_notification(user_id=None, message="", is_global=False, session=None):
        session = session or db.session
        try:
            notification = Notification(
                user_id=user_id,
                message=message,
                is_read=False,
                created_at=datetime.utcnow(),
                is_global=is_global
            )
            session.add(notification)
            session.commit()
        except Exception as e:
            print(f"Erro ao salvar notificação: {e}")
            session.rollback()


    @staticmethod
    def get_unread_notifications(user_id):
        notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
        
        return [
            {
                'id': n.id,
                'user_id': n.user_id,
                'message': n.message,
                'is_read': n.is_read,
                'created_at': n.created_at
            } for n in notifications
        ]

    @staticmethod
    def mark_notification_as_read(notification_id):
        notification = Notification.query.get(notification_id)
        if notification:
            notification.is_read = True
            db.session.commit()
