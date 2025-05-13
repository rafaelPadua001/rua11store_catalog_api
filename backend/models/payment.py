import sqlite3
from datetime import datetime
from controllers.stockController import StockController
import requests
import os
import uuid


class Payment:
    def __init__(self, payment_id, total_value, payment_date, payment_type, cpf, email, status, usuario_id, products, address=None):
        self.payment_id = payment_id
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
                    INSERT INTO payments (payment_id, total_value, payment_date, payment_type, cpf, email, status, usuario_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.payment_id,
                    self.total_value,
                    self.payment_date,
                    self.payment_type,
                    self.cpf,
                    self.email,
                    self.status,
                    self.usuario_id
                ))

                conn.commit()
                
                id = cursor.lastrowid

                cursor.execute(""" 
                    INSERT INTO orders(user_id, payment_id, shipment_info, total_amount, order_date)
                            VALUES(?, ?, ?, ?, datetime('now'))
                """,( self.usuario_id,
                    id,
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
                        id,
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
                        product_id,
                        quantity,
                        price,
                        self.total_value
                    ))

                # Se há endereço, criar uma entrega
                if self.address:
                    for product in self.products:
                        
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
                        
                    for product in self.products:
                        
                        product_id = product.get('id') if isinstance(product.get('id'), int) else product.get('product_id')
                        
                        stock_quantity = StockController.update_stock_quantity(product_id, quantity, conn=conn)
                        if 'error' in stock_quantity:
                            print(f"Erro ao atualizar o estoque para o produto {product_id}: {stock_quantity['error']}")
        except sqlite3.Error as e:
            print(f"Erro ao salvar o pagamento: {e}")
            conn.rollback()
        finally:
            conn.close()

    @staticmethod
    def update_status(self, payment_id, status):
        try:
            conn = self.get_db_connection() 
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE payments SET status = ? WHERE payment_id = ?",
                (status, payment_id)
            )
            conn.commit()
            updated = cursor.rowcount
            conn.close()

            if updated:
                print(f"Status do pagamento {payment_id} atualizado para {status}.")
                return True
            else:
                print(f"Pagamento com ID {payment_id} não encontrado.")
                return False
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
            return False
        
    @staticmethod
    def fetch_from_mercado_pago(payment_id, data=None):
        token = os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')
        
        url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            if data:
                # Atualização do pagamento (PUT)
                response = requests.put(url, headers=headers, json=data)
            else:
                # Consulta do pagamento (GET)
                response = requests.get(url, headers=headers)

            # Verifica se a resposta foi bem-sucedida
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Erro {response.status_code}: {response.text}")
        except Exception as e:
            # Retorna o erro de forma que a função sempre retorne um dicionário
            return {"error": str(e)}
        
    def payment_chargeback_mercado_pago(payment_id):
        token = os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')
        url = f"https://api.mercadopago.com/v1/payments/chargebacks/{payment_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Erro {response.status_code}: {response.text}")
        except Exception as e:
            return {"error": str(e)}
    
    def refund_payment_mercado_pago(payment_id, data):
        token = os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')
        url = f"https://api.mercadopago.com/v1/payments/{payment_id}/refunds"                 
        headers = { 
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Idempotency-Key": str(uuid.uuid4())
        }      
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Erro {response.status_code}: {response.text}")
        except Exception as e:
            return {"error": str(e)}
        