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
            "content": page.content,
            "heroTitle": page.hero_title,
            "heroSubtitle": page.hero_subtitle,
            "heroImage": page.hero_image,
            "carouselImages": page.carousel_images,
            "heroButtons": page.hero_buttons

        } for page in pages]

    @staticmethod
    def get_page_by_id(page_id):
        return Page.query.get(page_id)

    @staticmethod
    def get_page_by_title(page_title):
        return Page.query.filter_by(title=page_title).first()

    @staticmethod
    def create_page(page_data):
        new_page = Page(
            name=page_data.get('name', ''),
            title=page_data.get('title', ''),
            content=page_data.get('content', ''),
            hero_title=page_data.get('heroTitle', ''),
            hero_subtitle=page_data.get('heroSubtitle', ''),
            hero_background_color=page_data.get('heroBackgroundColor'),
            hero_image=page_data.get('heroImage', ''),
            hero_buttons=page_data.get('heroButtons', []),
            carousel_images=page_data.get('carouselImages', []),
            footer_text=page_data.get('footerText', '')
        )
        db.session.add(new_page)
        db.session.commit()
        return new_page


    @staticmethod
    def update_page(page_id, page_data):
        page = Page.query.get(page_id)
        if not page:
            return None

        if 'name' in page_data:
            page.name = page_data['name']
        if 'title' in page_data:
            page.title = page_data['title']
        if 'content' in page_data:
            page.content = page_data['content']
        if 'heroTitle' in page_data:
            page.hero_title = page_data['heroTitle']
        if 'heroSubtitle' in page_data:
            page.hero_subtitle = page_data['heroSubtitle']
        if 'heroBackgroundColor' in page_data:
            page.hero_background_color = page_data['heroBackgroundColor']
        if 'heroImage' in page_data:
            page.hero_image = page_data['heroImage']
        if 'heroButtons' in page_data:
            page.hero_buttons = page_data['heroButtons']
        if 'carouselImages' in page_data:
            page.carousel_images = page_data['carouselImages']
        if 'footerText' in page_data:
            page.footer_text = page_data['footerText']

        db.session.commit()
        return page


    @staticmethod
    def delete_page(page_id):
        page = Page.query.get(page_id)
        if page:
            db.session.delete(page)
            db.session.commit()
            return True
        return False
