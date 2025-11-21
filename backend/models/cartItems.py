from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class CartItems(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("client_users.id"), nullable=False)
    variation_data = db.Column(db.JSON, nullable=True)
    product_name = db.Column(db.Text, nullable=False)
    product_price = db.Column(db.Numeric(10, 2), nullable=False)
    product_image = db.Column(db.Text)
   

    product_height = db.Column(db.Numeric(10, 2))
    product_width = db.Column(db.Numeric(10, 2))
    product_weight = db.Column(db.Numeric(10, 2))
    product_length = db.Column(db.Numeric(10, 2))


    quantity = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relação com Product (para buscar mais info se precisar)
    product = db.relationship("Product", lazy=True)
    cart = db.relationship("Cart", back_populates="items")
