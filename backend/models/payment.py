import sqlite3
from models.delivery import Delivery
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

                for product in self.products:
                    if 'id' not in product:
                        print("Erro: 'id' não encontrado no produto:", product)
                        continue

                    price = float(product.get('price', 0))
                    quantity = int(product.get('quantity', 1))

                    cursor.execute("""
                        INSERT INTO payments_product(payment_id, product_id, product_name, product_quantity, product_price)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        payment_id,
                        product['id'],
                        product['name'],
                        quantity,
                        price
                    ))

                    # Se há endereço, criar uma entrega
                    if self.address:
                        for product in self.products:
                            delivery = Delivery(
                                product_id=product['id'],
                                user_id=self.usuario_id,
                                recipient_name=self.address.get('recipient_name'),
                                street=self.address.get('street'),
                                number=self.address.get('number'),
                                complement=self.address.get('complement'),
                                city=self.address.get('city'),
                                state=self.address.get('state'),
                                zip_code=self.address.get('zip_code'),
                                country=self.address.get('country'),
                                phone=self.address.get('phone'),
                                bairro=self.address.get('bairro')
                            )
                            cursor.execute("""
                                INSERT INTO delivery (product_id, user_id, recipient_name, street, number, complement, city, state, zip_code, country, phone, bairro)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                product['id'],
                                self.usuario_id,
                                self.address.get('recipient_name'),
                                self.address.get('street'),
                                self.address.get('number'),
                                self.address.get('complement'),
                                self.address.get('city'),
                                self.address.get('state'),
                                self.address.get('zip_code'),
                                self.address.get('country'),
                                self.address.get('phone'),
                                self.address.get('bairro')
                            ))

        except sqlite3.Error as e:
            print(f"Erro ao salvar o pagamento: {e}")
            conn.rollback()
        finally:
            conn.close()  # Garantir que a conexão será fechada

