import sqlite3
from datetime import datetime
from flask_socketio import SocketIO
from extensions import socketio



def get_db_connection():
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db', timeout=30.0)  # 10 segundos de timeout
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn

def create_notification(user_id, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notifications (user_id, message, read, created_at) VALUES (?, ?, ?, ?)",
        (user_id, message, False, datetime.utcnow())
    )
    conn.commit()
    conn.close()
    
    socketio.emit('new_notification', {'message': message})

def get_unread_notifications(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, message, created_at FROM notifications WHERE user_id = ? AND read = 0 ORDER BY created_at DESC",
        (user_id,)
    )
    result = cursor.fetchall()
    return [dict(row) for row in result]

def mark_notification_as_read(notification_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notifications SET read = 1 WHERE id = ?",
        (notification_id,)
    )
    conn.commit()
