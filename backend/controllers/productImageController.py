from models.productImage import ProductImage
from database import db

class ProductImageController:

    @staticmethod
    def create_images(product_id, image_paths, is_thumbnail=False):
        """Cria múltiplas imagens para um produto."""
        if not image_paths:
            return
        
        if isinstance(image_paths, str):
            image_paths = [image_paths]

        try:
            for path in image_paths:
                img = ProductImage(
                    product_id=product_id,
                    image_paths=path,   # nome da coluna correto
                    is_thumbnail=is_thumbnail
                )
                db.session.add(img)
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar imagens do produto: {str(e)}")
            raise

    @staticmethod
    def update_images(product_id, new_image_paths, is_thumbnail=False):
        """Atualiza as imagens de um produto, removendo as antigas e criando as novas."""
        try:
            # Deleta imagens antigas
            ProductImage.query.filter_by(product_id=product_id).delete()
            db.session.flush()  # para aplicar antes de inserir as novas
            
            # Normaliza new_image_paths para lista
            if not new_image_paths:
                new_image_paths = []
            elif isinstance(new_image_paths, str):
                new_image_paths = [new_image_paths]

            # Cria as novas imagens
            for path in new_image_paths:
                img = ProductImage(
                    product_id=product_id,
                    image_paths=path,
                    is_thumbnail=is_thumbnail
                )
                db.session.add(img)
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar imagens do produto: {str(e)}")
            raise

    @staticmethod
    def get_image_by_product(product_id):
        """Obtém as imagens de um produto pelo ID."""
        return ProductImage.query.filter_by(product_id=product_id).all()
    
    @staticmethod
    def delete_image_by_product(product_id):
        ProductImage.query.filter_by(product_id=product_id).delete()
        db.session.commit()
