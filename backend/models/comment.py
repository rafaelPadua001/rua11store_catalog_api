from datetime import datetime
from database import db

class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(100))
    avatar_url = db.Column(db.String(255))
    status = db.Column(db.String(20), nullable=False, default='pendente')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return{
            "id": self.id,
            'comment': self.comment,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "avatar_url": self.avatar_url,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }