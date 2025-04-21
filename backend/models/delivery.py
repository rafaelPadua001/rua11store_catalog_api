import sqlite3

class Delivery:
    def __init__(self, product_id, user_id, recipient_name, street, number, complement, city, state, zip_code, country, phone, bairro):
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

    def to_dict(self):
        return {
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
            "bairro": self.bairro
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
        cursor.execute("SELECT * FROM delivery")
        rows = cursor.fetchall()
        conn.close()

        deliveries = []
        for row in rows:
            delivery = Delivery(
                row['product_id'],   # ✅ Corrigido: product_id primeiro
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
                row['bairro']
            )
            deliveries.append(delivery.to_dict())

        return deliveries

    def save(self):
        conn = sqlite3.connect('database.db')
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO delivery (
                    product_id, user_id, recipient_name, street, number,
                    complement, city, state, zip_code, country, phone, bairro
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                self.bairro
            ))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao salvar a entrega: {e}")
            conn.rollback()
        finally:
            conn.close()
