from flask import Blueprint, request, jsonify, render_template
from models.blogPost import BlogPost
from models.page import Page
from controllers.blogController import BlogController
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

@blog_bp.route('/posts', methods=['GET'])
def get_post():
    return BlogController.get_posts()

@blog_bp.route('/posts', methods=['POST'])
def create_post():
    return BlogController.create_post()

@blog_bp.route('/posts/<int:postId>', methods=['PUT'])
def update_post(postId):
    if request.is_json:
        data = request.get_json()
    else:
        data = {**request.form.to_dict(), **request.files.to_dict()}
    return BlogController.update_post(postId, data)

@blog_bp.route('/posts/<int:postId>', methods=['DELETE'])
def delete_post(postId):
    return BlogController.delete_post(postId)