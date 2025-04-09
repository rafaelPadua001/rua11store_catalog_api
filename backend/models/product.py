import sqlite3

class Product:
    def __init__(self, id=None, name=None, description=None, price=None, 
                 category_id=None, subcategory_id=None, image_path=None, 
                 quantity=1, width=1, height=1, weight=1, user_id=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.image_path = image_path
        self.quantity = quantity
        self.width = width
        self.height = height
        self.weight = weight
        self.user_id = user_id  

    @staticmethod
    def get_db_connection():
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn

    def save(self):
        """Salva ou atualiza o produto no banco de dados"""
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            
            if self.id:
                # Atualiza o produto existente
                cursor.execute("""
                    UPDATE products 
                    SET name=?, description=?, price=?, category_id=?, 
                        subcategory_id=?, image_path=?, quantity=?, user_id=?
                    WHERE id=?
                """, (self.name, self.description, self.price, self.category_id, 
                      self.subcategory_id, self.image_path, self.quantity, 
                      self.user_id, self.id))
            else:
                # Insere um novo produto
                cursor.execute("""
                    INSERT INTO products (name, description, price, category_id, 
                                        subcategory_id, image_path, quantity, width,
                                height, weight, user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? , ?, ?)
                """, (self.name, self.description, self.price, self.category_id, 
                      self.subcategory_id, self.image_path, self.quantity, self.width,
                        self.height, self.weight, self.user_id))
                self.id = cursor.lastrowid  # Obtém o ID do produto recém-criado
            
            conn.commit()  # Aplica as alterações
            return True
            
        except sqlite3.Error as e:
            print(f"Erro ao salvar produto: {str(e)}")
            conn.rollback()  # Desfaz as alterações se houver erro
            return False
            
        finally:
            conn.close()  # Sempre fecha a conexão, mesmo em caso de erro

    def update(self, name, description, price, category_id, subcategory_id, quantity, width, height, weight, image_path):
        """Atualiza os dados de um produto existente no banco de dados"""
        if not self.id:
            print("Erro: Não é possível atualizar um produto sem ID.")
            return False

        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.quantity = quantity
        self.image_path = image_path
        self.width = width
        self.height = height
        self.weight = weight

        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE products 
                SET name=?, description=?, price=?, category_id=?, 
                    subcategory_id=?, image_path=?, quantity=?, width=?, height=?, weigth=?
                WHERE id=?
            """, (self.name, self.description, self.price, self.category_id, 
                self.subcategory_id, self.image_path, self.quantity, self.width,
                self.height, self.weight, self.id
            ))

            conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"Erro ao atualizar produto: {str(e)}")
            conn.rollback()
            return False

        finally:
            conn.close()


    def delete(self):
        """Exclui o produto do banco de dados"""
        if self.id:
            conn = self.get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products WHERE id = ?", (self.id,))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Erro ao excluir produto: {str(e)}")
                return False
            finally:
                conn.close()

    @staticmethod
    def get_all():
        """Obtém todos os produtos do banco de dados"""
        conn = Product.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            return [Product._create_from_row(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar produtos: {str(e)}")
            return []  # Retorna uma lista vazia em caso de erro
        finally:
            conn.close()

    @staticmethod
    def get_by_id(product_id):
        """Busca um produto pelo seu ID."""
        print(f"Buscando produto com ID: {product_id}")
        conn = Product.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product_data = cursor.fetchone()
            return Product._create_from_row(product_data) if product_data else None
        except sqlite3.Error as e:
            print(f"Erro de banco de dados: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise
        finally:
            conn.close()

    @staticmethod
    def find_by_id_and_user(product_id, user_id):
        conn = Product.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ? AND user_id = ?", (product_id, user_id))
        result = cursor.fetchone()

        if result:
            return Product(*result)  # Ajuste conforme a estrutura da sua classe
        return None
    @staticmethod
    def get_by_user(user_id):
        """Obtém produtos associados a um usuário específico"""
        conn = Product.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE user_id = ?", (user_id,))
            return [Product._create_from_row(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar produtos por usuário: {str(e)}")
            return []  # Retorna uma lista vazia em caso de erro
        finally:
            conn.close()

    @staticmethod
    def _create_from_row(row):
        """Cria uma instância de Product a partir de uma linha do banco de dados"""
        if row is None:
            return None
        return Product(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            price=row['price'],
            category_id=row['category_id'],
            subcategory_id=row['subcategory_id'],
            image_path=row['image_path'],
            quantity=row['quantity'],
            user_id=row['user_id']
        )

    def to_dict(self):
        """Converte a instância de Product em um dicionário"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category_id": self.category_id,
            "subcategory_id": self.subcategory_id,
            "image_path": self.image_path,
            "quantity": self.quantity,
            "user_id": self.user_id
        }