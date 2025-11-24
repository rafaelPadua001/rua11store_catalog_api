from database import db
from datetime import datetime
import uuid

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(
        db.String(64),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)

    # Novos campos necessários
    type = db.Column(db.String(50), nullable=False, default='client')  
    fcm_token = db.Column(db.Text, nullable=True)

    # Datas
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    
    # Relacionamento 1:1 com UserProfile (antes chamado ProfileModel)
    profile = db.relationship('UserProfile', back_populates='user', uselist=False)
