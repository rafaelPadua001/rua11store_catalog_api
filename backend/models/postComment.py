from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database import db
import uuid

class PostComment(db.Model):
    __tablename__ = 'post_comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('blog_posts.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=True, default=None)
    username = Column(String(100), nullable=True)
    user_avatar = Column(String(500), nullable=True)
    login_provider = Column(String(50), nullable=True)
    text = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    post = db.relationship("BlogPost", back_populates="comments")

    def to_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "username": self.username,
            "user_avatar": self.user_avatar,
            "login_provider": self.login_provider,
            "text": self.text,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
