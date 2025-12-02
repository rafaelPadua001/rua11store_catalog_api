from datetime import datetime
from database import db



class BlogPostView(db.Model):
    __tablename__ = "post_views"
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    post = db.relationship("BlogPost", back_populates='views')

    def to_dict(self, include_post=False):
        data = {
            "id": self.id,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

        if include_post and self.post:
            data["post"] = {
                "id": self.post.id,
                "title": self.post.title,
                "slug": self.post.slug
            }

        return data
