from flask import Blueprint, request, jsonify, render_template
from models.blogPost import BlogPost
from models.page import Page
#from controllers.categoryController import CategoryController
from flask_cors import CORS

# Criação do Blueprint
blog_bp = Blueprint('blog', __name__)

# Configuração Global do CORS para esse Blueprint
CORS(blog_bp, 
     resources={
         r"/*": {
             "origins": [
                 "https://rua11store-catalog-api.vercel.app",
                 "http://localhost:3000"
             ],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }
     })

@blog_bp.route('/blog')
def blog_index():
    blog_page = Page.query.filter_by(name="blog").first_or_404()
    posts = BlogPost.query.filter_by(page_id=blog_page.id)\
            .order_by(BlogPost.created_at.desc())\
            .all()
    return render_template('blog/index.html', page=blog_page, posts=posts)

@blog_bp.route('/blog/<slug>')
def blog_details(slug):
    post = BlogPost.query.filter_by(slug=slug).first_or_404()
    return render_template("blog/detail.html", post=post, page=post.page)
