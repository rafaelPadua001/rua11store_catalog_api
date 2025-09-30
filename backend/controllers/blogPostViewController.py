from flask import jsonify
from database import db
from models.blogPost import BlogPost
from models.blogPostView import  BlogPostView

def add_view(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()

    new_view = BlogPostView(post_id=post.id)
    db.session.add(new_view)
    db.session.commit()

    return jsonify({'message': 'view registered with success !'})