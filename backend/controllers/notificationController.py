from models.notification import Notification
from database import db
from datetime import datetime
class NotificationController:
    @staticmethod
    def create_notification(user_id=None, message="", is_global=False, session=None):
        session = session or db.session
        try:
            # se a model Notification tem agora user_uuid, ajuste:
            notification = Notification(
                user_id=None,              # manter compatibilidade com coluna antiga
                user_uuid=str(user_id) if user_id else None,
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
        notifications = Notification.query.filter(
            (Notification.user_uuid == str(user_id)) | (Notification.is_global == True),
            Notification.is_read == False
        ).order_by(Notification.created_at.desc()).all()
        
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
