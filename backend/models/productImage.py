from database import db

class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_path = db.Column(db.String, nullable=False)  # Caminho para a imagem do produto
    is_thumbnail = db.Column(db.Boolean, default=False)  # Indica se a imagem é a miniatura
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


    def save(self):
        db.sessioon.add(self)
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'image_path': self.image_path,
            'is_thumbnail': self.is_thumbnail,
            'created_at': self.created_at.isoformat() if self.created_at else None  
        }