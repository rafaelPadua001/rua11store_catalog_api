import sqlite3

class Delivery:
    def __init__(self, id, product_id, user_id, recipient_name, street, number,
                  complement, city, state, zip_code, country, phone, bairro, total_value,
                delivery_id, width=None, height=None, length=None, weight=None, cpf=None, melhorenvio_id=None, order_id=None):
        self.id = id
        self.product_id = product_id
        self.user_id = user_id
        self.recipient_name = recipient_name
        self.street = street
        self.number = number
        self.complement = complement
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone = phone
        self.bairro = bairro
        self.total_value = total_value
        self.delivery_id = delivery_id
        self.width = width  
        self.height = height  
        self.length = length  
        self.weight = weight 
        self.cpf = cpf
        self.melhorenvio_id = melhorenvio_id
        self.order_id = order_id

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "recipient_name": self.recipient_name,
            "street": self.street,
            "number": self.number,
            "complement": self.complement,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
            "phone": self.phone,
            "bairro": self.bairro,
            "total_value": self.total_value,
            "delivery_id": self.delivery_id,
            "width": self.width,  
            "height": self.height,  
            "length": self.length,  
            "weight": self.weight,
            "cpf": self.cpf,
            "melhorenvio_id": self.melhorenvio_id,
            'order_id': self.order_id
        }
    @staticmethod
    def get_db_connection():
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn

    @staticmethod
    def get_all():
        conn = Delivery.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                    d.id AS id,
                    d.recipient_name,
                    d.complement AS complement,
                    d.street,
                    d.number,
                    d.city,
                    d.state,
                    d.zip_code,
                    d.country,
                    d.phone,
                    d.bairro,
                    d.total_value AS total_value,
                    d.width,
                    d.height,
                    d.length,
                    d.weight,
                    d.melhorenvio_id,
                    d.order_id AS order_id,

                    o.id,
                    o.user_id,
                    o.payment_id,
                    o.delivery_id,
                    o.shipment_info,
                    o.total_amount AS order_total,
                    o.order_date,
                    o.status,

                    pay.id AS payment_id,
                    pay.cpf AS cpf,
                    pay.email AS email,
                    

                    oi.id AS item_id,
                    oi.product_id,
                    oi.quantity,
                    oi.unit_price,
                    oi.total_price,

                    p.name AS product_name,
                    p.description AS product_description,
                    p.image_path AS product_image
                    

                FROM 
                    delivery d
                INNER JOIN
                    orders o ON d.id = o.delivery_id
                LEFT JOIN 
                    order_items oi ON o.id = oi.order_id
                LEFT JOIN
                    products p ON oi.product_id = p.id
                LEFT JOIN
                    payments AS pay ON o.payment_id = pay.id

                ORDER BY 
                    d.id DESC;



        """)
        rows = cursor.fetchall()
        conn.close()

        deliveries_dict = {}

        for row in rows:
            delivery_id = row['id']

            # Se ainda não adicionamos esse delivery, criamos a entrada
            if delivery_id not in deliveries_dict:
                delivery_dict = {
                    'id': delivery_id,
                    'recipient_name': row['recipient_name'],
                    'street': row['street'],
                    'number': row['number'],
                    'complement': row['complement'],
                    'city': row['city'],
                    'state': row['state'],
                    'zip_code': row['zip_code'],
                    'country': row['country'],
                    'phone': row['phone'],
                    'bairro': row['bairro'],
                    'total_value': row['total_value'],
                    'width': row['width'],
                    'height': row['height'],
                    'length': row['length'],
                    'weight': row['weight'],
                    'melhorenvio_id': row['melhorenvio_id'],
                    'order_id': row['order_id'],
                    'user_id': row['user_id'],
                    'payment_id': row['payment_id'],
                    'cpf': row['cpf'],
                    'email': row['email'],
                    'order_total': row['order_total'],
                    'order_date': row['order_date'],
                    'status': row['status'],
                    'products': []  # importante inicializar apenas uma vez
                }

                deliveries_dict[delivery_id] = delivery_dict

            # Sempre adiciona o produto
            deliveries_dict[delivery_id]['products'].append({
                'product_id': row['product_id'],
                'name': row['product_name'],
                'description': row['product_description'],
                'image': row['product_image'],
                'price': row['unit_price'],
                'quantity': row['quantity'] or 1
            })

        # Retorna apenas os valores únicos (com lista de produtos agregada)
        return list(deliveries_dict.values())


    def save(self):
        conn = sqlite3.connect('database.db')
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO delivery (
                    product_id, user_id, recipient_name, street, number,
                    complement, city, state, zip_code, country, phone, bairro, total_value, delivery_id,
                    width, height, length, weight
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.product_id,
                self.user_id,
                self.recipient_name,
                self.street,
                self.number,
                self.complement,
                self.city,
                self.state,
                self.zip_code,
                self.country,
                self.phone,
                self.bairro,
                self.total_value,
                self.delivery_id,
                self.width,  
                self.height,  
                self.length,  
                self.weight,  
            ))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao salvar a entrega: {e}")
            conn.rollback()
        finally:
            conn.close()

    def update(shipment_data):
        print('Shipment ', shipment_data)
        try:
            conn = Delivery.get_db_connection()
            cursor = conn.cursor()
            cursor.execute( cursor.execute("""
                UPDATE delivery SET
                    status = ?,
                    service_status = ?,
                    state_abbr = ?,
                    company_name = ?,
                    tracking_link = ?
                WHERE melhorenvio_id = ?
            """, (
                shipment_data['status'],
                shipment_data['service_status'],
                shipment_data['state_abbr'],
                shipment_data['company_name'],
                shipment_data['tracking_link'],
                shipment_data['melhorenvio_id']
            )))

            conn.commit()
            conn.close()

            print(f"Delivery {melhorenvio_id} atualizado com sucesso")
            return True
        except Exception as e:
            print(f'Erro ao atualizar entrega: ${e}')
            return False