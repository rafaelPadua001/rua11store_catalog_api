import sqlite3
from datetime import datetime
from flask_socketio import SocketIO
from extensions import socketio



def get_db_connection():
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db', timeout=30.0)  # 10 segundos de timeout
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn

def create_notification(user_id=None, message="", is_global=False, conn=None):
    internal_conn = conn or sqlite3.connect('database.db', timeout=30.0)
    
    try:
        with internal_conn:
            cursor = internal_conn.cursor()
            cursor.execute("""
                INSERT INTO notifications (message, is_read, created_at, is_global)
                VALUES (?, 0, datetime('now'), ?)
            """, (message, int(is_global)))
    except Exception as e:
        print(f"Erro ao salvar notificação: {e}")
    finally:
        if conn is None:
            internal_conn.close()

def get_unread_notifications(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, message, created_at
        FROM notifications
        WHERE (user_id = ? OR is_global = 1)
          AND is_read = 0
        ORDER BY created_at DESC
        """,
        (user_id,)
    )
    result = cursor.fetchall()
    conn.close()
    return [dict(row) for row in result]


def mark_notification_as_read(notification_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notifications SET is_read = 1 WHERE id = ?",
        (notification_id,)
    )
    conn.commit()
