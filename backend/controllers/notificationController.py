from models.notification import Notification
from database import db

class NotificationController:
    @staticmethod
    def create_notification(user_id, message):
        notification = Notification(user_id=user_id, message=message)
        db.session.add(notification)
        db.session.commit()

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
