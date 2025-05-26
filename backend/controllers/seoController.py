import sqlite3
from models.seo import Seo

class SeoController:
    def get_db_connection():
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db', timeout=30.0)
        conn.row_factory = sqlite3.Row
        return conn
    @staticmethod
    def get_all_seo():
        db = SeoController.get_db_connection()
        rows = db.execute("SELECT * FROM seo_pages").fetchall()
        seo_items = []

        for row in rows:
            seo_item = Seo.from_row(row)
            seo_items.append(seo_item.to_dict())

        return seo_items
    
    @staticmethod
    def save_seo(seo: Seo):
        route_id = seo.get('route', {}).get('id')  # Ou 'name', 'id', etc.

        db = SeoController.get_db_connection()
        db.execute(
            "INSERT INTO seo_pages (route, title, description, keywords, og_title, og_description, og_image) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (route_id, seo['metaTitle'], seo['metaDescription'], seo['metaKeywords'], seo['ogTitle'], seo['ogDescription'], seo['ogImage'])
        )
        db.commit()

    @staticmethod
    def update_seo(seo_id, seo: Seo):
        db = SeoController.get_db_connection()
        db.execute(
            "UPDATE seo_pages SET route = ?, title = ?, description = ?, keywords = ?, og_title = ?, og_description = ?, og_image = ? WHERE id = ?",
            (seo['route'], seo['metaTitle'], seo['metaDescription'], seo['metaKeywords'], seo['ogTitle'], seo['ogDescription'], seo['ogImage'], seo_id)
        )
        db.commit()

    @staticmethod
    def delete_seo(seo_id):
        db = SeoController.get_db_connection()
        db.execute("DELETE FROM seo_pages WHERE id = ?", (seo_id,))
        db.commit()