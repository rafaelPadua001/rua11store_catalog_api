import sqlite3

class Delivery:
    def __init__(self, id, user_id, product_id, recipient_name, street, number, complement,
                 city, state, zip_code, country, phone):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.recipient_name = recipient_name
        self.street = street
        self.number = number
        self.complement = complement
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone = phone

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
            deliveries.append(
                Delivery(
                    row['id'],
                    row['user_id'],
                    row['product_id'],
                    row['recipient_name'],
                    row['street'],
                    row['number'],
                    row['complement'],
                    row['city'],
                    row['state'],
                    row['zip_code'],
                    row['country'],
                    row['phone']
                )
            )
        return deliveries
    
    @staticmethod
    def create(user_id, product_id, recipient_name, street, number, complement,
               city, state, zip_code, country, phone):
        conn = Delivery.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO delivery (
                user_id, product_id, recipient_name, street, number, complement,
                city, state, zip_code, country, phone
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, product_id, recipient_name, street, number, complement,
            city, state, zip_code, country, phone
        ))
        conn.commit()
        conn.close()

