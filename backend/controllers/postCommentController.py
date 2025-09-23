from flask import jsonify, request
from database import db
from models.postComment import PostComment
import uuid

class PostCommentController:
    @staticmethod
    def get_comments():
        comments = PostComment.query.all()
        return jsonify([comment.to_dict() for comment in comments]), 200
    @staticmethod
    def save_comment():
        data = request.json

        post_id = data.get('post_id')
        text = data.get('text')
        user_id = data.get('user_id')
        if user_id:
            user_id = uuid.UUID(user_id)

        username = data.get('username')
        user_avatar = data.get('user_avatar')
        login_provider = data.get('login_provider')

        if not post_id or not text:
            return jsonify({'error':"post_id e text são obrigátorios"}), 400
        
        comment = PostComment(
            post_id=post_id,
            text=text,
            user_id=user_id,
            username=username,
            user_avatar=user_avatar,
            login_provider=login_provider
        )

        db.session.add(comment)
        db.session.commit()
        
        return jsonify({"message": "Comentário criado com sucesso", "comment": comment.to_dict()}), 200
    
    @staticmethod
    def get_comments_by_postId(postId):
        comments = PostComment.query.filter_by(post_id=postId).order_by(PostComment.created_at.desc()).all()
        return jsonify([comment.to_dict() for comment in comments]), 200
    

    @staticmethod
    def report_comment(commentId):
        comment = PostComment.query.get(commentId)
        if not comment:
            return {'error': 'Comentário não encontrado'}, 400
        
        comment.status = 'reported'
        db.session.commit()
        
        return {
            "message": "Comentário reportado para a moderação",
            "id": comment.text,
            "status": comment.status
        }, 200
    
       

    @staticmethod
    def remove_comment(commentId):
        comment = PostComment.query.get_or_404(commentId)
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comentário removido com sucesso'}), 200
    
       