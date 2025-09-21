from database import db
from sqlalchemy import Numeric
from sqlalchemy.orm import joinedload
from models.productSeo import ProductSeo
from models.stock import Stock
from models.productSeo import ProductSeo
from models.comment import Comment
from models.productImage import ProductImage
from models.productVideo import ProductVideo


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    price = db.Column(Numeric(10,2))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    subcategory_id = db.Column(db.Integer)
    thumbnail_path = db.Column(db.String)  # Caminho para a imagem de miniatura
    image_paths = db.Column(db.String)
   # video_path = db.Column(db.String)  # Caminho para o vídeo do produto
    quantity = db.Column(db.Integer, default=1)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    length = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    category = db.relationship("Category", back_populates="products")
    stock = db.relationship('Stock', back_populates='product', uselist=False)
    seo = db.relationship('ProductSeo', uselist=False, back_populates='product', cascade="all, delete-orphan")
    images = db.relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    
    def save(self):
        """Salva ou atualiza o produto"""
        try:
            if not self.id:
                db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Erro ao salvar produto: {e}")
            db.session.rollback()
            return False

    def update(self, **kwargs):
        """Atualiza campos do produto"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()

    def delete(self):
        """Exclui o produto"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar produto: {e}")
            db.session.rollback()
            return False

    @staticmethod
    def get_all():
        try:
           
            results = db.session.query(
                Product,
                ProductImage,
                ProductVideo,
                Stock.product_quantity,
                ProductSeo,
                Comment
            ).join(
                Stock, Product.id == Stock.id_product
            ).outerjoin(
                ProductSeo, Product.id == ProductSeo.product_id
            ).outerjoin(
                Comment, Product.id == Comment.product_id
            ).outerjoin(
                ProductImage, Product.id == ProductImage.product_id
            ).outerjoin(
                ProductVideo, Product.id == ProductVideo.product_id
            ).all()

            product_map = {}

            for product, product_image, product_video, quantity, seo, comment in results:
                pid = product.id

                if pid not in product_map:
                    product_map[pid] = {
                        "product": {
                            "id": product.id,
                            "name": product.name,
                            "description": product.description,
                            "price": str(product.price),
                            "thumbnail_path": product.thumbnail_path,
                            "category_id": product.category_id,
                            "subcategory_id": product.subcategory_id,
                            "user_id": product.user_id,
                            "length": product.length,
                            "width": product.width,
                            "height": product.height,
                            "weight": product.weight,
                            "quantity": product.quantity,
                        },
                        "product_images": [],
                        "product_videos": [],
                        "product_quantity": quantity,
                        "seo": {
                            "meta_title": seo.meta_title if seo else None,
                            "meta_description": seo.meta_description if seo else None,
                            "slug": seo.slug if seo else None,
                            "keywords": seo.keywords if seo else None
                        } if seo else None,
                        "comments": [],
                    }

                # Adiciona imagens (todas as encontradas)
                if product_image:
                    product_map[pid]["product_images"].append({
                        "id": product_image.id,
                        "product_id": product_image.product_id,
                        "image_path": product_image.image_path,
                        "is_thumbnail": product_image.is_thumbnail,
                        "created_at": product_image.created_at.isoformat() if product_image.created_at else None
                    })

                # adiciona videos (todos encontrados)
                if product_video:
                    product_map[pid]["product_videos"].append({
                        "id": product_video.id,
                        "product_id": product_video.product_id,
                        "video_path":   product_video.video_path,
                        "created_at": product_video.created_at,
                    })

                # Adiciona comentários (todos)
                if comment:
                    product_map[pid]["comments"].append({
                        "id": comment.id,
                        "product_id": comment.product_id,
                        "user_id": comment.user_id,
                        "user_name": comment.user_name,
                        "avatar_url": comment.avatar_url,
                        "comment": comment.comment,
                        "status": comment.status,
                        "created_at": comment.created_at.isoformat() if comment.created_at else None,
                        "updated_at": comment.updated_at.isoformat() if comment.updated_at else None
                    })

            return list(product_map.values())

        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            return []
    
    @staticmethod
    def get_by_id(product_id):
        try:
            return Product.query.get(product_id)
        except Exception as e:
            print(f"Erro ao buscar produto por ID: {e}")
            return None
        
    @staticmethod
    def get_by_slug(slug):
        try:
            # Busca o SEO pelo slug
            seo = ProductSeo.query.filter_by(slug=slug).first()

            if not seo:
                print(f'Slug não encontrado: {slug}')
                return None

            # Agora busca o Product pelo product_id
            product = Product.query.get(seo.product_id)

            if not product:
                print(f'Produto com ID {seo.product_id} não encontrado.')
                return None

            return product

        except Exception as e:
            print(f'Erro ao buscar produto por slug: {e}')
            return None

        
    @staticmethod
    def find_by_id_and_user(product_id, user_id):
        try:
            return Product.query.filter_by(id=product_id, user_id=user_id).first()
        except Exception as e:
            print(f"Erro ao buscar produto por ID e usuário: {e}")
            return None

    @staticmethod
    def get_by_user(user_id):
        try:
            return Product.query.filter_by(user_id=user_id).all()
        except Exception as e:
            print(f"Erro ao buscar produtos do usuário: {e}")
            return []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": getattr(self, "description", None),
            "price": f"{self.price:.2f}" if isinstance(self.price, float) else self.price,
            "category_id": getattr(self, "category_id", None),
            "subcategory_id": getattr(self, "subcategory_id", None),
            "image_paths": getattr(self, "image_paths", None),
            "thumbnail_path": getattr(self, "thumbnail_path", None),
            "product_images": [
            {
                    "id": img.id,
                    "product_id": img.product_id,
                    "image_path": img.image_path,
                    "is_thumbnail": img.is_thumbnail,
                    "created_at": img.created_at.isoformat() if img.created_at else None
                }
                for img in getattr(self, "product_images", [])
            ],
           "product_video": None if not getattr(self, "product_videos", None) else {
                "id": self.product_videos[0].id,
                "product_id": self.product_videos[0].product_id,
                "video_path": self.product_videos[0].image_path,
                "created_at": self.product_videos[0].created_at.isoformat() if self.product_videos[0].created_at else None
            },
            "category": self.category.to_dict() if self.category else None,
            "quantity": self.quantity,
            "width": getattr(self, "width", None),
            "height": getattr(self, "height", None),
            "weight": getattr(self, "weight", None),
            "length": getattr(self, "length", None),
            "user_id": getattr(self, "user_id", None),
            "seo": self.seo.to_dict() if self.seo and hasattr(self.seo, "to_dict") else (
                {
                    "meta_title": getattr(self.seo, "meta_title", None),
                    "meta_description": getattr(self.seo, "meta_description", None),
                    "slug": getattr(self.seo, "slug", None),
                    "keywords": getattr(self.seo, "keywords", None),
                } if self.seo else None
            ),
            "comments": [c.to_dict() for c in self.comments] if getattr(self, "comments", None) else []
        }
    
    def to_dict_basic(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": f"{self.price:.2f}" if isinstance(self.price, float) else self.price,
            "thumbnail_path": self.thumbnail_path,
            "category_id": self.category_id
        }
