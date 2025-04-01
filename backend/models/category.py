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
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn

    def save(self):
        """Salva ou atualiza a categoria no banco de dados"""
        conn = Category.get_db_connection()
        try:
            cursor = conn.cursor()
            
            if self.id:
                # Atualiza a categoria existente
                cursor.execute("""
                    UPDATE categories 
                    SET name=?, is_subcategory=?, parent_id=?, user_id=?
                    WHERE id=?
                """, (self.name, self.is_subcategory, self.parent_id, self.user_id, self.id))
            else:
                # Insere uma nova categoria
                cursor.execute("""
                    INSERT INTO categories (name, is_subcategory, parent_id, user_id)
                    VALUES (?, ?, ?, ?)
                """, (self.name, self.is_subcategory, self.parent_id, self.user_id))
                self.id = cursor.lastrowid  # Obtém o ID da categoria recém-criada
            
            conn.commit()  # Aplica as alterações
            return True
            
        except sqlite3.Error as e:
            print(f"Erro ao salvar categoria: {str(e)}")
            conn.rollback()  # Desfaz as alterações se houver erro
            return False
            
        finally:
            conn.close()  # Sempre fecha a conexão, mesmo em caso de erro

    def delete(self):
        """Exclui a categoria do banco de dados"""
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
        """Obtém todas as categorias do banco de dados"""
        conn = Category.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories")
            return [Category._create_from_row(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar categorias: {str(e)}")
            return []  # Retorna uma lista vazia em caso de erro
        finally:
            conn.close()

    @staticmethod
    def get_by_id(category_id):
        """Busca uma categoria pelo seu ID."""
        print(f"Buscando categoria com ID: {category_id}")
        try:
            conn = Category.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
            category_data = cursor.fetchone()
            conn.close()

            if category_data:
                return Category(
                    id=category_data[0],
                    name=category_data[1],
                    is_subcategory=category_data[2],
                    parent_id=category_data[3],
                    user_id=category_data[4]
                )
            return None

        except sqlite3.Error as e:
            print(f"Erro de banco de dados: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise

    @staticmethod
    def get_by_user(user_id):
        """Obtém categorias associadas a um usuário específico"""
        conn = Category.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories WHERE user_id = ?", (user_id,))
            return [Category._create_from_row(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar categorias por usuário: {str(e)}")
            return []  # Retorna uma lista vazia em caso de erro
        finally:
            conn.close()

    @staticmethod
    def _create_from_row(row):
        """Cria uma instância de Category a partir de uma linha do banco de dados"""
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
        """Converte a instância de Category em um dicionário"""
        return {
            "id": self.id,
            "name": self.name,
            "is_subcategory": self.is_subcategory,
            "parent_id": self.parent_id,
            "user_id": self.user_id
        }
