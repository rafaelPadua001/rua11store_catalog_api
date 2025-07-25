from database import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import joinedload




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
    
    @staticmethod
    def get_by_slug(slug):
        from models.product import Product

        try:
            seo = ProductSeo.query.options(joinedload(ProductSeo.product)).filter_by(slug=slug).first()

            if not seo:
                return {"error": "Slug não encontrado"}, 404

            product = seo.product

            if not product:
                return {"error": "Produto não encontrado"}, 404

            return {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": product.quantity,
                    "description": product.description,
                    # outros campos
                },
                "seo": {
                    "slug": seo.slug,
                    "meta_title": seo.meta_title,
                    "meta_description": seo.meta_description,
                    "keywords": seo.keywords,
                }
            }

        except Exception as e:
            print(f'Erro ao buscar produto por slug: {e}')
            return {"error": "Erro interno"}, 500
