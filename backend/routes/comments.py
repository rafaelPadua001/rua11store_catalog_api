from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from controllers.commentController import CommentController
from flask_cors import CORS

comments_bp = Blueprint('comments', __name__)

CORS(comments_bp, resources={r"/comments/*": {"origins": "*"}}, supports_credentials=True)

@comments_bp.route('/comments', methods=['GET'])
@jwt_required()
def getComments():
    return CommentController.get_all()

@comments_bp.route('/new', methods=['POST'])
def newComment():
    try: 
        data = request.get_json()

        #basic validate
        comment = data.get('comment')
        product_id = data.get('product_id')
        status = data.get('status')
        user_id = data.get('user_id')
        user_name = data.get('user_name')
        avatar_url = data.get('avatar_url')

        if not comment or not product_id or not status:
            return jsonify({'error': 'dados incompletos'}), 400

        result = CommentController.create_comment(comment, product_id, user_id, user_name, avatar_url, status)

        return jsonify({'message': 'Comentário criado com sucesso', 'comment': result}), 201   
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@comments_bp.route('/update/<int:comment_id>', methods=['PUT'])
def updateComment(comment_id):
    data = request.get_json()

    updated_comment, error = CommentController.update_comment(comment_id, data)
    if error:
        if error == "Comment not found":
            return jsonify({"error": error}), 404
        return jsonify({"error:", error}), 500
    return jsonify(updated_comment), 200

@comments_bp.route('/delete/<int:comment_id>', methods=['DELETE'])
def deleteComment(comment_id):
    success, error = CommentController.delete_by_id(comment_id)
    if not success:
        if error == "Comment not found":
            return jsonify({"error"> error}), 404
        return jsonify({"error": error}), 500
    return jsonify({"message": "Comment deleted succcessfully"}), 200
  