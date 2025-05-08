import sqlite3

class Stock:
    def __init__(self, id=None, id_product=None, user_id=None, category_id=None, product_name=None,
                 product_price=None, product_quantity=None, variations=None):
        self.id = id
        self.id_product = id_product
        self.user_id = user_id
        self.category_id = category_id
        self.product_name = product_name
        self.product_price = product_price
        self.product_quantity = product_quantity
        self.variations = variations

    @staticmethod
    def get_db_connection():
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn

    @staticmethod
    def create(data):
        """Adiciona um novo item ao estoque"""
        query = """
            INSERT INTO stock (id_product, user_id, category_id, product_name, product_price, product_quantity,
                variations, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """

        conn = Stock.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (
            data['id_product'],
            data['user_id'],
            data['category_id'],
            data['product_name'],
            data['product_price'],
            data['product_quantity'],
            data.get('variations', None)
        ))
        
        conn.commit()
        stock_id = cursor.lastrowid  # Pega o ID gerado
        conn.close()
        return stock_id

    @staticmethod
    def get_all():
        """Busca todos os itens do estoque"""
        query = "SELECT * FROM stock"
        conn = Stock.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(stock_id):
        """Busca um item do estoque pelo ID"""
        query = "SELECT * FROM stock WHERE id = ?"
        conn = Stock.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (stock_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    
    @staticmethod
    def get_stock_id_by_product(id_product):
        """Retorna o stock_id associado a um id_product"""
        query = "SELECT id FROM stock WHERE id_product = ?"
        conn = Stock.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (id_product,))
        stock = cursor.fetchone()
        conn.close()
        return stock["id"] if stock else None  # Retorna None se não encontrar

    @staticmethod
    def update(stock_id, data):
        """Atualiza um item do estoque"""
        query = """UPDATE stock 
                   SET id_product = ?, user_id = ?, category_id = ?, product_name = ?, 
                       product_price = ?, product_quantity = ?, variations = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?"""

        conn = Stock.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (
            data['id_product'],
            data['user_id'],
            data['category_id'],
            data['product_name'],
            data['product_price'],
            data['product_quantity'],
            data.get('variations', None),
            stock_id
        ))
        
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated
    
    @staticmethod
    def update_stock_quantity(product_id, quantity, conn=None):
        """Atualiza a quantidade de um item do estoque"""
        should_close = False
        if conn is None:
            conn = Stock.get_db_connection()
            should_close = True

        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(""" 
                SELECT product_quantity, id FROM stock WHERE id_product = ?
            """, (product_id,))
            row = cursor.fetchone()

            if row is None:
                return False
            
            current_quantity = row['product_quantity']
            new_quantity = current_quantity - quantity

            if new_quantity < 0:
                return {"error": "Quantidade insuficiente em estoque"}

            cursor.execute(
                "UPDATE stock SET product_quantity = ? WHERE id = ?",
                (new_quantity, row['id'])
            )
            conn.commit()

            return {
                "stock_id": row['id'],
                "old_quantity": current_quantity,
                "new_quantity": new_quantity
            }
        finally:
            if should_close:
                conn.close()


    @staticmethod
    def delete(stock_id):
        """Remove um item do estoque"""
        query = "DELETE FROM stock WHERE id = ?"
        conn = Stock.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (stock_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
