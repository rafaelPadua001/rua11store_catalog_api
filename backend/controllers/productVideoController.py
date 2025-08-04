from models.productVideo import ProductVideo
from database import db

class ProductVideoController:

    @staticmethod
    def create_video(product_id, video_path):
        """Cria um vídeo para um produto."""
        video = ProductVideo(product_id=product_id, video_path=video_path)
        try:
            db.session.add(video)
            db.session.commit()
            return video
        except Exception as e:
            print(f"Erro ao criar vídeo do produto: {e}")
            db.session.rollback()
            return None
        
    @staticmethod
    def update_video(product_id, new_video_path):
        """Atualiza o vídeo de um produto. Se não existir, cria um novo."""
        video = ProductVideo.query.filter_by(product_id=product_id).first()
        try:
            if video:
                video.video_path = new_video_path
            else:
                video = ProductVideo(product_id=product_id, video_path=new_video_path)
                db.session.add(video)
            db.session.commit()
            return video
        except Exception as e:
            print(f"Erro ao atualizar vídeo do produto: {e}")
            db.session.rollback()
            return None


    @staticmethod
    def get_video_by_product(product_id):
        """Obtém o vídeo de um produto pelo ID."""
        return ProductVideo.query.filter_by(product_id=product_id).first()

    @staticmethod
    def delete_video_by_product(product_id):
        """Deleta o vídeo de um produto pelo ID."""
        ProductVideo.query.filter_by(product_id=product_id).delete()
        db.session.commit()