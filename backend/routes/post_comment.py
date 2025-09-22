from flask import Blueprint, jsonify, request
from controllers.postCommentController import PostCommentController

postComment_bp = Blueprint('post-comment', __name__)

@postComment_bp.route('/post-comment', methods=['POST'])
def create_comment():
    return PostCommentController.save_comment()

@postComment_bp.route('/post-comment/<int:postId>', methods=['GET'])
def get_comments_by_postId(postId):
    return PostCommentController.get_comments_by_postId(postId)
  