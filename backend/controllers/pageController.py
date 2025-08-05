from models.page import Page
from database import db

class PageController:

    @staticmethod
    def get_all_pages():
        pages = Page.query.all()
        return [{
            "id": page.id,
            "name": page.name,
            "title": page.title,
            "content": page.content
        } for page in pages]

    @staticmethod
    def get_page_by_id(page_id):
        return Page.query.get(page_id)

    @staticmethod
    def get_page_by_name(page_name):
        return Page.query.filter_by(name=page_name).first()

    @staticmethod
    def create_page(page_data):
        new_page = Page(
            name=page_data['name'],
            title=page_data['title'],
            content=page_data['content']
        )
        db.session.add(new_page)
        db.session.commit()
        return new_page

    @staticmethod
    def update_page(page_id, page_data):
        page = Page.query.get(page_id)
        if page:
            page.name = page_data['name']
            page.title = page_data['title']
            page.content = page_data['content']
            db.session.commit()
            return page
        return None

    @staticmethod
    def delete_page(page_id):
        page = Page.query.get(page_id)
        if page:
            db.session.delete(page)
            db.session.commit()
            return True
        return False
