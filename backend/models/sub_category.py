import sqlite3

class SubCategory:
    def __init__(self, id=None, name=None, category_id=None):
        self.id = id
        self.name = name
        self.category_id

        @staticmethod
        def get_db_connection():
            conn = sqlite3.connect('database.db')
            conn.row_factory = sqlite3.Row
            return conn
        
        def save(self):
            conn = self.get_db_connection()
            cursor = conn.cursor

            if seld.id:
                cursor.execute("""
                    UPDATE subcategories 
                    SET name = ?, category_id = ? 
                    WHERE id = ?
                """, (self.name, self.category_id, self.id))
            else:
                cursor.execute("""
                    INSERT INTO subcategories (name, category_id) 
                    VALUES (?, ?)
                """, (self.name, self.category_id))
                self.id = cursor.lastrowid

            conn.commit()
            conn.close()

        def delete(self):
            if self.id:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELTE FROM subcategories WHERE id = ?", (self.id))
                conn.commit()
                conn.close()

        @staticmethod
        def get_all():
            conn = SubCategory.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subcategories")
            subcategories = cursor.fetchall()
            conn.close()
            return [dict(row) for row in subcategory]

        @staticmethod
        def get_by_id(subcategory_id):
            conn = SubCategory.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subcategories WHERE id = ?", (subcategory_id))
            subcategory = cursor.fetchone()
            conn.close()
            return dict(subcategory) if subcategory else None
       
        @classmethod
        def get_by_category(cls, category_id):
            # Implemente a lógica para buscar subcategorias por category_id
            # Exemplo com SQLAlchemy:
            return cls.query.filter_by(category_id=category_id).all()