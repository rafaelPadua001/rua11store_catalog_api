from database import db
from datetime import datetime

class PostSeo(db.Model):
    __tablename__ = "post_seo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"), nullable=False, unique=True)

    keywords = db.Column(db.String(255))
    description = db.Column(db.String(255))
    canonical_url = db.Column(db.String(255))
    og_title = db.Column(db.String(255))
    og_description = db.Column(db.String(255))
    og_image = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relacionamento inverso
    post = db.relationship("BlogPost", back_populates="seo_metadata")
