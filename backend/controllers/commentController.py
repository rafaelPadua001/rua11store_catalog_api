from models.comment import Comment
from database import db
from datetime import datetime
from models import Product
class CommentController:
    def __init__(self):
        # Usar a sessão do Flask-SQLAlchemy direto
        self.db_session = db.session

    def get_all():
        try:
            comments = Comment.query.all()
            result = []
            for comment in comments:
                # Buscar produto relacionado ao product_id do comment
                product = Product.query.filter_by(id=comment.product_id).first()
                comment_dict = comment.to_dict()
                # Adicionar os dados do produto no dicionário do comentário
                comment_dict['product'] = product.to_dict() if product else None
                result.append(comment_dict)
            return result
        except Exception as e:
            print(f"Erro ao buscar comentarios: {e}")
            return []


    def create_comment(comment, product_id, user_id, user_name, avatar_url, status):
        new_comment = Comment(
            comment=comment,
            product_id=product_id,
            user_id=user_id,
            user_name=user_name,
            avatar_url=avatar_url,
            status=status
        )

        db.session.add(new_comment)
        db.session.commit()
        return new_comment.to_dict()
    
    def update_comment(comment_id, data):
        comment = Comment.query.get(comment_id)
        if not comment:
            return None, "Comment not found"
        
        if 'comment' in data:
            comment.comment = data['comment']
        if 'product_id' in data:
            comment.product_id = data['product_id']
        if 'user_id' in data:
            comment.user_id = data['user_id']
        if 'user_name' in data:
            comment.user_name = data['user_name']
        if 'status' in data:
            comment.status = data['status']

        comment.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            return comment.to_dict(), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_by_id( comment_id):
        comment = Comment.query.get(comment_id)
        if not comment:
            return False

        try:

            db.session.delete(comment)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
