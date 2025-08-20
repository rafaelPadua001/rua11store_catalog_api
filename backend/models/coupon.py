from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from database import db

class Coupon(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    client_id = db.Column(pg.UUID(as_uuid=True), nullable=False)
    client_username = db.Column(db.String, nullable=True) 
    title = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False, unique=True)
    discount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    image_path = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'client_id': self.client_id,
            'client_username': self.client_username,
            'title': self.title,
            'code': self.code,
            'discount': self.discount,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'image_path': self.image_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            user_id=data["user_id"],
            client_id=data["client_id"],
            client_username=data.get("client_username"),
            title=data["title"],
            code=data["code"],
            discount=data["discount"],
            start_date=datetime.fromisoformat(data["start_date"]) if data.get("start_date") else None,
            end_date=datetime.fromisoformat(data["end_date"]) if data.get("end_date") else None,
            image_path=data.get("image_path"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
        )
