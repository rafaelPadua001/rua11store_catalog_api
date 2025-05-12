import sqlite3
from datetime import datetime
# from controllers.orderController import orderController


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
    
    @staticmethod
    def get_all():
        orders = {}
        conn = Order.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(""" 
            SELECT 
                o.id AS order_id,
                o.user_id,
                o.payment_id,
                o.shipment_info,
                o.total_amount AS order_total,
                o.order_date,
                o.status,
                oi.id AS item_id,
                oi.product_id,
                oi.quantity,
                oi.unit_price,
                oi.total_price,
                p.name AS product_name,
                p.description as product_description,
                p.price as product_price,
                p.image_path as product_image       
            FROM 
                orders o
            JOIN 
                order_items oi ON o.id = oi.order_id
            JOIN
                products p ON oi.product_id = p.id
            ORDER BY 
                o.id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            order_id = row['order_id']
            
            # Se ainda não adicionamos esse pedido ao dicionário, criamos ele
            if order_id not in orders:
                orders[order_id] = Order(
                    id=row['order_id'],
                    user_id=row['user_id'],
                    payment_id=row['payment_id'],
                    shipment_info=row['shipment_info'],
                    order_date=row['order_date'],
                    total_amount=row['order_total'],
                    status=row['status'],
                    items=[]
                )

            # Adiciona o item à lista de items da order
            orders[order_id].items.append({
                "item_id": row['item_id'],
                "product_id": row['product_id'],
                "quantity": row['quantity'],
                "unit_price": row['unit_price'],
                "total_price": row['total_price'],
                "product_name": row['product_name'],
                "product_description": row['product_description'],
                "product_image": row['product_image']
            })

        # Converte cada pedido em dicionário
        return [order.to_dict() for order in orders.values()]


    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "payment_id": self.payment_id,
            "shipment_info": self.shipment_info,
            "order_date": self.order_date,
            "status": self.status,
            "total_amount": self.total_amount,
            "items": self.items  # já é uma lista de dicionários
        }


        
   
    def get_order_by_userId(user_id):
        try:
            print(f"Buscando pedidos para o usuário com ID: {user_id}")  # Log para verificar o user_id
            conn = Order.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    o.id AS order_id,
                    o.user_id,
                    o.payment_id,
                    o.shipment_info,
                    o.total_amount AS order_total,
                    o.order_date,
                    o.status,
                    oi.id AS item_id,
                    oi.product_id,
                    oi.quantity,
                    oi.unit_price,
                    oi.total_price,
                    p.name AS product_name,
                    p.description AS product_description,
                    p.price AS product_price,
                    p.image_path AS product_image
                FROM 
                    orders o
                JOIN 
                    order_items oi ON o.id = oi.order_id
                JOIN
                    products p ON oi.product_id = p.id
                WHERE
                    o.user_id = ?
                ORDER BY 
                    o.id DESC
            """, (user_id,))

            results = cursor.fetchall()
            
            conn.close()

            if results:
               
                orders = {}
                for row in results:
                    order_id = row[0]

                    
                    if order_id not in orders:
                        orders[order_id] = {
                            'order_id': row[0],
                            'user_id': row[1],
                            'payment_id': row[2],
                            'shipment_info': row[3],
                            'order_total': row[4],
                            'order_date': row[5],
                            'status': row[6],
                            'items': []
                        }

                   
                    orders[order_id]['items'].append({
                        'item_id': row[7],
                        'product_id': row[8],
                        'quantity': row[9],
                        'unit_price': row[10],
                        'total_price': row[11],
                        'product_name': row[12],
                        'product_description': row[13],
                        'product_price': row[14],
                        'product_image': row[15]
                    })

                return list(orders.values())
            else:
                return None

        except Exception as e:
            print(f"Erro ao buscar os pedidos e itens: {str(e)}")  # Log para capturar erro
            raise Exception(f"Erro ao buscar os pedidos e itens: {str(e)}")



    

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
