from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from database import db

class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref='carts')
    items = db.relationship("CartItems", back_populates="cart", lazy=True, cascade="all, delete-orphan")
    