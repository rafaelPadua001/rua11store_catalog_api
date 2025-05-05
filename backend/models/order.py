import sqlite3
from datetime import datetime


class Order:
    def __init__(self, id, user_id, payment_id, shipment_info, order_date, items , total_amount, status=None):
        self.id = id
        self.user_id = user_id
        self.payment_id = payment_id
        self.shipment_info = shipment_info
        self.order_date = order_date
        self.status = status
        self.total_amount = total_amount
        self.items = items  # lista de dicionários com "product_id", "quantity", "unit_price"
        

    @staticmethod
    def get_db_connection():
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db', timeout=30.0)  # 10 segundos de timeout
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn
    
    def get_all():
        orders = []
        conn = Order.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(""" 
            SELECT * FROM orders
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            order = Order(
                row['id'],
                row['user_id'],
                row['payment_id'],
                row['shipment_info'],
                row['order_date'],
                row['status'],
                row['total_amount']
            )
        orders_dict = order.to_dict()
        orders.append(orders_dict)

        return orders

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "payment_id": self.payment_id,
            "shipment_info": self.shipment_info,
            "order_date": self.order_date,
            "status": self.status,
            "total_amount": self.total_amount
        }

    def save(self):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Inserir na tabela orders
            cursor.execute("""
                INSERT INTO orders (user_id, payment_id, shipment_info, total_amount, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (self.user_id, self.payment_id, self.shipment_info, self.total_amount, datetime.now()))

            # Pegar o ID do pedido
            order_id = cursor.lastrowid

            # Inserir os itens do pedido
            for item in self.items:
                product_id = item['product_id']
                quantity = item['quantity']
                unit_price = item['unit_price']
                total_price = unit_price * quantity

                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                """, (order_id, product_id, quantity, unit_price, total_price))

            conn.commit()
            conn.close()

            return order_id  # Retorna o ID do pedido criado

        except Exception as e:
            raise Exception(f"Erro ao salvar o pedido: {str(e)}")
