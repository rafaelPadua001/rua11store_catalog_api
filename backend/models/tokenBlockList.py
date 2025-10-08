from datetime import datetime
from database import db  # Seu objeto SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    user_id = db.Column(db.String(36), nullable=False, index=True)  # ⚡ String para ambos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TokenBlocklist {self.jti}>'