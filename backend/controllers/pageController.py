import sqlite3
from models.page import Page

class PageController:

    @staticmethod
    def get_db_connection():
            """Cria uma nova conexão com o banco de dados"""
            conn = sqlite3.connect('database.db', timeout=30.0)  # 10 segundos de timeout
            conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
            return conn

    def get_all_pages():
        db = PageController.get_db_connection()
        rows = db.execute("SELECT * FROM pages").fetchall()
        pages = []

        for row in rows:
            page = {
                "id": row["id"],
                "name": row["name"],
                "title": row["title"],
                "content": row["content"]
            }
            pages.append(page)

        return pages

    def get_page_by_id(page_id):
        db = PageController.get_db_connection()
        row = db.execute("SELECT * FROM pages WHERE id = ?", (page_id,)).fetchone()
        if row:
            return Page(id=row["id"], name=row['name'], title=row["title"], content=row["content"])
        return None

    def get_page_by_name(page_name):
        db = PageController.get_db_connection()
        row = db.execute("SELECT * FROM pages WHERE name = ?", (page_name,)).fetchone()
        if row:
            return Page(id=row["id"], name=row['name'], title=row["title"], content=row["content"])
        return None
    
    def create_page(page: Page):
        db = PageController.get_db_connection()
        db.execute("INSERT INTO pages (name, title, content) VALUES (?, ?, ?)", (page['name'], page['title'], page['content']))
        db.commit()


    def update_page(page_id, page: Page):
        db = PageController.get_db_connection()
        db.execute(
            "UPDATE pages SET name = ?, title = ?, content = ? WHERE id = ?",
            (page['name'], page['title'], page['content'], page['id'])
        )
        db.commit()


    def delete_page(page_id: int):
        db = PageController.get_db_connection()
        db.execute("DELETE FROM pages WHERE id = ?", (page_id,))
        db.commit()
