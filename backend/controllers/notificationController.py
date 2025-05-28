import sqlite3

class NotificationController:
    @staticmethod
    def get_db_connection():
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db', timeout=30.0)  # 10 segundos de timeout
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn

    def create_notification(user_id, message):
        conn = NotificationController.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notifications (user_id, message) VALUES (?, ?)", (user_id, message))
        conn.commit()

    def get_unread_notifications(user_id):
        conn = NotificationController.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notifications WHERE user_id = ? AND is_read = 0", (user_id,))
        return [dict(row) for row in cursor.fetchall()]

    def mark_notification_as_read(notification_id):
        conn = NotificationController.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notification_id,))
        conn.commit()
