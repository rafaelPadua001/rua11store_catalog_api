import sqlite3

class Produto:
    def __init__(self, id=None, nome=None, descricao=None, preco=None, estoque=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque

    @classmethod
    def buscar_todos(cls):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, descricao, preco, estoque FROM produtos")
        produtos = []
        for row in cursor.fetchall():
            produtos.append(cls(*row))
        conn.close()
        return produtos

    # Adicione outros métodos conforme necessário