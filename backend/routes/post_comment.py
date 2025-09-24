from flask import Blueprint, jsonify, request
from flask_cors import CORS
from controllers.postCommentController import PostCommentController

postComment_bp = Blueprint('post-comment', __name__)

CORS(postComment_bp, resources={r"/post-comment/*": {"origins": "*"}}, supports_credentials=True)

@postComment_bp.route('/post-comment', methods=['GET'])
def get_comments():
    return PostCommentController.get_comments()

@postComment_bp.route('/post-comment', methods=['POST'])
def create_comment():
    return PostCommentController.save_comment()

@postComment_bp.route('/post-comment/<int:postId>', methods=['GET'])
def get_comments_by_postId(postId):
    return PostCommentController.get_comments_by_postId(postId)

@postComment_bp.route('/post-comment/post-comment-report/<int:commentId>', methods=['POST'])
def report_comment(commentId):
    return PostCommentController.report_comment(commentId)

@postComment_bp.route('/post-comment/comment-alter-status/<int:commentId>', methods=["POST", "OPTIONS"])
def alter_status(commentId):
    if request.method == 'OPTIONS':
        return '', 200  # responde ao preflight

    return PostCommentController.alter_status_comment(commentId)

@postComment_bp.route('/post-comment/<int:commentId>', methods=['DELETE'])
def delete_comment(commentId):
    return PostCommentController.remove_comment(commentId)
  