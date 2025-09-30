from flask import Blueprint
from controllers.blogPostViewController import add_view, get_views

post_views_bp = Blueprint('post_views', __name__)

@post_views_bp.route('/post-views/<int:post_id>', methods=['POST'])
def register_view(post_id):
    return add_view(post_id)