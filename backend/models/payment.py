import sqlite3
from models.delivery import Delivery
from models.order import Order
from datetime import datetime

class Payment:
    def __init__(self, total_value, payment_date, payment_type, cpf, email, status, usuario_id, products, address=None):
        self.total_value = total_value
        self.payment_date = payment_date or datetime.now().isoformat()
        self.payment_type = payment_type
        self.cpf = cpf
        self.email = email
        self.status = status
        self.usuario_id = usuario_id
        self.products = products
        self.address = address
    
    @staticmethod
    def get_db_connection():
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db', timeout=30.0)  # 10 segundos de timeout
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn
    
    @staticmethod
    def get_all_payments():
        conn = Payment.get_db_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(""" 
                SELECT * FROM payments ORDER BY payment_date DESC
            """)
            rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def save(self):
        conn = self.get_db_connection()
        try:
            with conn:
                cursor = conn.cursor()

                # Inserir pagamento
                cursor.execute("""
                    INSERT INTO payments (total_value, payment_date, payment_type, cpf, email, status, usuario_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.total_value,
                    self.payment_date,
                    self.payment_type,
                    self.cpf,
                    self.email,
                    self.status,
                    self.usuario_id
                ))

                payment_id = cursor.lastrowid

                cursor.execute(""" 
                    INSERT INTO orders(user_id, payment_id, shipment_info, total_amount, order_date)
                            VALUES(?, ?, ?, ?, datetime('now'))
                """,( self.usuario_id,
                    payment_id,
                    self.address.get('zip_code', '') if self.address else '',
                    self.total_value
                ))

                order_id = cursor.lastrowid

                # Inserir os produtos do pagamento
                for product in self.products:
                    if 'id' not in product:
                        print("Erro: 'id' não encontrado no produto:", product)
                        continue
                    product_id = product.get('id') if isinstance(product.get('id'), int) else product.get('product_id')

                    
                    
                    product_name = product.get('name') or product.get('product_name')
                    if not product_name:
                        raise ValueError("Nome do produto ausente")

                    price = float(product.get('price', 0))
                    quantity = int(product.get('quantity', 1))

                    cursor.execute("""
                        INSERT INTO payments_product(payment_id, product_id, product_name, product_quantity, product_price)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        payment_id,
                        product_id,
                        product_name,
                        quantity,
                        price
                    ))
                       # order_items
                    cursor.execute("""
                        INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        order_id,
                        product['id'],
                        quantity,
                        price,
                        self.total_value
                    ))

                # Se há endereço, criar uma entrega
                if self.address:
                    for product in self.products:
                        print(f"Address product: {product}")
                        cursor.execute("""
                            INSERT INTO delivery (
                                product_id, user_id, recipient_name, street, number,
                                complement, city, state, zip_code, country, phone, bairro,
                                total_value, delivery_id, width, height, length, weight
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            product['id'],
                            self.usuario_id,
                            self.address.get('recipient_name', ''),
                            self.address.get('street', ''),
                            self.address.get('number', ''),
                            self.address.get('complement', ''),
                            self.address.get('city', ''),
                            self.address.get('state', ''),
                            self.address.get('zip_code', ''),
                            self.address.get('country', ''),
                            self.address.get('phone', ''),
                            self.address.get('bairro', ''),
                            self.address.get('total_value', 0),
                            self.address.get('delivery_id', ''),
                            product.get('width', 0),
                            product.get('height', 0),
                            product.get('length', 0),
                            product.get('weight', 0)
                        ))

        except sqlite3.Error as e:
            print(f"Erro ao salvar o pagamento: {e}")
            conn.rollback()
        finally:
            conn.close()
