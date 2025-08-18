from database import db
from sqlalchemy.dialects.postgresql import JSON


class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    hero_title = db.Column(db.String(255), nullable=True)
    hero_subtitle = db.Column(db.String(255), nullable=True)
    hero_background_color = db.Column(db.String(50), nullable=True)
    hero_image = db.Column(db.String(500), nullable=True)
    hero_buttons = db.Column(JSON, nullable=True)
    carousel_images = db.Column(JSON, nullable=True)
    footer_text = db.Column(db.Text, nullable=True)

    def __init__(
        self, name, title, content="", hero_title="",
        hero_subtitle="", hero_background_color="", hero_image="",   hero_buttons=None, carousel_images=None, footer_text=""
    ):
        self.name = name
        self.title = title
        self.content = content
        self.hero_title = hero_title
        self.hero_subtitle = hero_subtitle
        self.hero_background_color = hero_background_color
        self.hero_image = hero_image
        self.hero_buttons = hero_buttons
        self.carousel_images = carousel_images or []
        self.footer_text = footer_text
