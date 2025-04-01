import sqlite3

class Category:
    def __init__(self, id=None, name=None, is_subcategory=False, parent_id=None):
        self.id = id
        self.name = name
        self.is_subcategory = is_subcategory
        self.parent_id = parent_id

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn

    def save(self):
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            
            if self.id:
                # Atualização
                cursor.execute("""
                    UPDATE categories 
                    SET name=?, is_subcategory=?, parent_id=?
                    WHERE id=?
                """, (self.name, self.is_subcategory, self.parent_id, self.id))
            else:
                # Inserção
                cursor.execute("""
                    INSERT INTO categories (name, is_subcategory, parent_id)
                    VALUES (?, ?, ?)
                """, (self.name, self.is_subcategory, self.parent_id))
                self.id = cursor.lastrowid  # Captura o ID gerado
            
            conn.commit()
            return True  # Retorna True em caso de sucesso
            
        except sqlite3.Error as e:
            print(f"Erro ao salvar categoria: {str(e)}")
            conn.rollback()
            return False  # Retorna False em caso de erro
            
        finally:
            conn.close()

    def delete(self):
        if self.id:
            conn = self.get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM categories WHERE id = ?", (self.id,))
                conn.commit()
            finally:
                conn.close()

    @staticmethod
    def get_all():
        conn = Category.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories")
            categories = cursor.fetchall()
            return [dict(row) for row in categories]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(category_id):
        conn = Category.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
            category = cursor.fetchone()
            
            if category:
                # Retorna uma INSTÂNCIA de Category, não um dicionário
                return Category(
                    id=category['id'],
                    name=category['name'],
                    is_subcategory=bool(category['is_subcategory']),
                    parent_id=category['parent_id']
                )
            return None
        finally:
            conn.close()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_subcategory": self.is_subcategory,
            "parent_id": self.parent_id
        }