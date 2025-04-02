import sqlite3

class Product:
    def __init__(self, id=None, name=None, description=None, price=None, 
                 category_id=None, subcategory_id=None, image_path=None, 
                 quantity=1, user_id=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.image_path = image_path
        self.quantity = quantity
        self.user_id = user_id

    def save(self):
        """Salva o produto no banco de dados"""
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, description, price, category_id, subcategory_id, image_path, quantity, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.name, self.description, self.price, self.category_id, 
              self.subcategory_id, self.image_path, self.quantity, self.user_id))
        
        conn.commit()
        conn.close()

    @classmethod
    def get_all(cls):
        """Busca todos os produtos"""
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, description, price, category_id, subcategory_id, 
                   image_path, quantity, user_id 
            FROM products
        """)
        products = [cls(*row) for row in cursor.fetchall()]
        conn.close()
        return products
