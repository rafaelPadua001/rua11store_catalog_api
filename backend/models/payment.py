import sqlite3

class Payment:
    def __init__(self, total_value, payment_date, payment_type, cpf, email, status, usuario_id, products):
        self.total_value = total_value
        self.payment_date = payment_date or datetime.now().isoformat()
        self.payment_type = payment_type
        self.cpf = cpf
        self.email = email
        self.status = status
        self.usuario_id = usuario_id
        self.products = products
    
    @staticmethod
    def get_db_connection():
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn

    def save(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Inserir pagamento com status
        cursor.execute(""" 
            INSERT INTO payments(total_value, payment_date, payment_type, cpf, email, status, usuario_id)
                VALUES(?, ?, ?, ?, ?, ?, ?)
        """, (
            self.total_value,
            self.payment_date,
            self.payment_type,
            self.cpf,
            self.email,
            self.status,  # Agora o status é inserido
            self.usuario_id
        ))

        payment_id = cursor.lastrowid  # Corrigido para 'lastrowid'

        # Verificando os dados de 'products' antes de salvar
        for product in self.products:
            print(product)  # Debug: verificar a estrutura de cada 'product'
            if 'id' not in product:
                print("Erro: 'id' não encontrado no produto:", product)
                continue  # Pular esse produto se não encontrar o 'id'

            # Garantir que os valores de 'price' e 'quantity' sejam float e int, respectivamente
            price = float(product.get('price', 0))
            quantity = int(product.get('quantity', 1))

            cursor.execute("""
                INSERT INTO payments_product(payment_id, product_id, product_name, product_quantity, product_price)
                    VALUES(?, ?, ?, ?, ?)
            """, (
                payment_id,
                product['id'],  # Agora estamos usando 'id' em vez de 'product_id'
                product['name'],
                quantity,
                price
            ))

        conn.commit()
        conn.close()
