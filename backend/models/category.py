import sqlite3

class Category:
    def __init__(self, id=None, name=None, is_subcategory=False, parent_id=None, user_id=None):
        self.id = id
        self.name = name
        self.is_subcategory = is_subcategory
        self.parent_id = parent_id
        self.user_id = user_id  

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn

    def save(self):
        conn = Category.get_db_connection()
        try:
            cursor = conn.cursor()
            
            if self.id:
                cursor.execute("""
                    UPDATE categories 
                    SET name=?, is_subcategory=?, parent_id=?, user_id=?
                    WHERE id=?
                """, (self.name, self.is_subcategory, self.parent_id, self.user_id, self.id))
            else:
                cursor.execute("""
                    INSERT INTO categories (name, is_subcategory, parent_id, user_id)
                    VALUES (?, ?, ?, ?)
                """, (self.name, self.is_subcategory, self.parent_id, self.user_id))
                self.id = cursor.lastrowid
            
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Erro ao salvar categoria: {str(e)}")
            conn.rollback()
            return False
            
        finally:
            conn.close()

    def delete(self):
        if self.id:
            conn = Category.get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM categories WHERE id = ?", (self.id,))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Erro ao excluir categoria: {str(e)}")
                return False
            finally:
                conn.close()

    @staticmethod
    def get_all():
        conn = Category.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories")
            return [Category._create_from_row(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar categorias: {str(e)}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(category_id):
        conn = Category.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
            row = cursor.fetchone()
            return Category._create_from_row(row) if row else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar categoria por ID: {str(e)}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = Category.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories WHERE user_id = ?", (user_id,))
            return [Category._create_from_row(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar categorias por usuário: {str(e)}")
            return []
        finally:
            conn.close()

    @staticmethod
    def _create_from_row(row):
        if row is None:
            return None
        return Category(
            id=row['id'],
            name=row['name'],
            is_subcategory=bool(row['is_subcategory']),
            parent_id=row['parent_id'] if row['parent_id'] is not None else None,
            user_id=row['user_id'] if row['user_id'] is not None else None
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_subcategory": self.is_subcategory,
            "parent_id": self.parent_id,
            "user_id": self.user_id
        }
