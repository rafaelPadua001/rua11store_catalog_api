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
                d.*, 
                p.id AS payment_id,
                p.email, 
                p.cpf,
                pp.product_name, 
                pp.product_price,
                pp.product_quantity
            FROM delivery d
            LEFT JOIN payments p ON d.user_id = p.usuario_id
            LEFT JOIN payments_product pp ON pp.payment_id = p.id
        """)
        rows = cursor.fetchall()
        conn.close()

        deliveries_dict = {}

        for row in rows:
            delivery_id = row['id']

            if delivery_id not in deliveries_dict:
                # Cria o objeto e dicionário da entrega
                delivery = Delivery(
                    row['id'],
                    row['product_id'],   
                    row['user_id'],
                    row['recipient_name'],
                    row['street'],
                    row['number'],
                    row['complement'],
                    row['city'],
                    row['state'],
                    row['zip_code'],
                    row['country'],
                    row['phone'],
                    row['bairro'],
                    row['total_value'],
                    row['delivery_id'],
                    row['width'],  
                    row['height'],  
                    row['length'],  
                    row['weight'],
                    row['cpf'],
                    row['melhorenvio_id'],
                    row['order_id']
                )

                delivery_dict = delivery.to_dict()
                delivery_dict['email'] = row['email']
                delivery_dict['cpf'] = row['cpf']
                delivery_dict['melhorenvio_id'] = row['melhorenvio_id']
                delivery_dict['order_id'] = row['order_id']
                delivery_dict['products'] = []  # Aqui armazenaremos todos os produtos

                deliveries_dict[delivery_id] = delivery_dict

            # Adiciona o produto à lista se existir
            if row['product_name'] and row['product_price'] is not None:
                deliveries_dict[delivery_id]['products'].append({
                    'name': row['product_name'],
                    'price': row['product_price'],
                    'quantity': row['product_quantity'] or 1
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