import sqlite3
from models.coupon import Coupon
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from models.coupon import Coupon


class CouponController:
    @staticmethod
    def get_db_connection():
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db', timeout=30.0)  # 10 segundos de timeout
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn
    
    def get_all_coupons(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM coupons')
        rows = cursor.fetchall()
        conn.close()
        return [Coupon.from_row(row) for row in rows]

    def create_coupon(self, user_id, client_id, title, code, discount, start_date, end_date, image_path=None):
        now = datetime.utcnow().isoformat()
        conn = self.get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Verifica se já existe cupom com o mesmo código
        cursor.execute('SELECT id FROM coupons WHERE code = ?', (code,))
        if cursor.fetchone():
            conn.close()
            raise Exception("Já existe um cupom com esse código.")

        # Inserir cupom
        cursor.execute('''
            INSERT INTO coupons (
                user_id, client_id, title, code, discount, start_date, end_date, image_path, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, client_id, title, code, discount, start_date, end_date, image_path, now, now))

        conn.commit()  # <-- ESSENCIAL

        coupon_id = cursor.lastrowid

        # Buscar o cupom recém-criado
        cursor.execute('SELECT * FROM coupons WHERE id = ?', (coupon_id,))
        row = cursor.fetchone()
        conn.close()

        # Criar e retornar instância da classe Coupon
        return Coupon.from_row(row)


    def update_coupon(self, coupon_id, user_id, client_id, title, code, discount, start_date, end_date, image_path=None):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM coupons WHERE id = ?', (coupon_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None  # ou lançar Exception

        # Atualiza o cupom
        cursor.execute('''
            UPDATE coupons SET
                user_id = ?,
                client_id = ?,
                title = ?,
                code = ?,
                discount = ?,
                start_date = ?,
                end_date = ?,
                image_path = ?,
                updated_at = ?
            WHERE id = ?
        ''', (user_id, client_id, title, code, discount, start_date, end_date, image_path, datetime.utcnow().isoformat(), coupon_id))

        conn.commit()

        # Retorna o cupom atualizado
        cursor.execute('SELECT * FROM coupons WHERE id = ?', (coupon_id,))
        updated_coupon = cursor.fetchone()
        conn.close()

        # Converte o resultado em dicionário
        if updated_coupon:
            return self.row_to_dict(updated_coupon)
        return None
    
    def row_to_dict(self, row):
        return {
            'id': row['id'],
            'user_id': row['user_id'],
            'client_id': row['client_id'],
            'title': row['title'],
            'code': row['code'],
            'discount': row['discount'],
            'start_date': row['start_date'],
            'end_date': row['end_date'],
            'image_path': row['image_path'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at']
    }

       
    def delete_coupon(self, coupon_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM coupons WHERE id = ?', (coupon_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None  # ou lançar Exception

        cursor.execute('DELETE FROM coupons WHERE id = ?', (coupon_id,))
        conn.commit()
        conn.close()

        return Coupon.from_row(row)  # Retorna o cupom deletado como confirmação
       
        
      