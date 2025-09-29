from datetime import datetime
from database import db
from models.page import Page
class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_id = db.Column(db.Integer, db.ForeignKey("pages.id"), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)

    title = db.Column(db.String(255), nullable=False)
    excerpt = db.Column(db.String(300), nullable=True)
    content = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    page = db.relationship('Page', backref=db.backref("articles", lazy=True))
    seo_metadata = db.relationship("PostSeo", uselist=False, back_populates="post", cascade="all, delete-orphan")
    comments = db.relationship(
        "PostComment",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy=True
    )
