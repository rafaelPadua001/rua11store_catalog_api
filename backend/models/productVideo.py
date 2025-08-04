from database import db

class ProductVideo(db.Model):
    __tablename__ = 'product_videos'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    video_path = db.Column(db.String, nullable=False)  # Caminho para o vídeo do produto
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def save(self):
        """Salva ou atualiza o vídeo do produto"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Erro ao salvar vídeo do produto: {e}")
            db.session.rollback()
            return False

    def to_dict(self):
        """Converte o objeto para um dicionário"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'video_path': self.video_path,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }