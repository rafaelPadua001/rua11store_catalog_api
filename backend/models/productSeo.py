from database import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class ProductSeo(db.Model):
    __tablename__ = 'product_seo'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), unique=True, nullable=False)
    meta_title = db.Column(db.String(255))
    meta_description = db.Column(db.Text)
    slug = db.Column(db.String(255))
    keywords = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = db.relationship('Product', back_populates='seo')

    def __repr__(self):
        return f'<ProductSeo {self.meta_title}>'