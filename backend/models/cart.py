from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from database import db

class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # user_id agora é UUID
    user_id = db.Column(db.Uuid(as_uuid=True), db.ForeignKey("client_users.id"), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relações
    user = db.relationship("ClientUser", backref='carts')
    items = db.relationship(
        "CartItems",
        back_populates="cart",
        lazy=True,
        cascade="all, delete-orphan"
    )
