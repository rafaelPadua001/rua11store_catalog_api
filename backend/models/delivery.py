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
    
    def save(self):
        # Lógica para salvar a instância Delivery no banco de dados
        conn = sqlite3.connect('database.db')
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO delivery (product_id, user_id, recipient_name, street, number, complement, city, state, zip_code, country, phone, bairro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
