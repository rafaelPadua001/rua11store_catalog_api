from database import db
from sqlalchemy import Numeric
from sqlalchemy.orm import joinedload
from models.productSeo import ProductSeo
from models.stock import Stock
from models.productSeo import ProductSeo
from models.comment import Comment
from models.productImage import ProductImage
from models.productVideo import ProductVideo
from models.variation import Variation


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    comments = db.relationship("Comment", back_populates="product")

    videos = db.relationship("ProductVideo", back_populates="product", cascade="all, delete-orphan")
    variations = db.relationship(
        "Variation",
        back_populates="product",
        lazy="joined",
        cascade="all, delete-orphan"
    )

    order_items = db.relationship('OrderItem', back_populates='product', passive_deletes=True)

    def save(self):
        try:
            db.session.add(self)        # Sempre adiciona à sessão
            db.session.commit()         # Commit gera o ID no banco
            db.session.refresh(self)    # Atualiza o objeto com o ID gerado
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
            products = Product.query.options(
                joinedload(Product.images),
                joinedload(Product.stock),
                joinedload(Product.seo),
                joinedload(Product.comments),
                joinedload(Product.variations),
                joinedload(Product.videos)
            ).all()

            product_list = []

            for p in products:
                item = {
                    "product": {
                        "id": p.id,
                        "name": p.name,
                        "description": p.description,
                        "price": str(p.price),
                        "thumbnail_path": p.thumbnail_path,
                        "category_id": p.category_id,
                        "subcategory_id": p.subcategory_id,
                        "user_id": p.user_id,
                        "length": p.length,
                        "width": p.width,
                        "height": p.height,
                        "weight": p.weight,
                        "quantity": p.quantity,
                        "sizes": [],
                        "colors": [],
                    },
                    "product_images": [{"id": img.id, "image_path": img.image_path} for img in p.images],
                    "product_videos": [{"id": vid.id, "video_path": vid.video_path} for vid in getattr(p, "videos", [])],
                    "product_quantity": getattr(p.stock, "product_quantity", 0),
                    "seo": {
                        "meta_title": p.seo.meta_title if p.seo else None,
                        "meta_description": p.seo.meta_description if p.seo else None,
                        "slug": p.seo.slug if p.seo else None,
                        "keywords": p.seo.keywords if p.seo else None
                    } if p.seo else None,
                    "comments": [{"id": c.id, "comment": c.comment} for c in getattr(p, "comments", [])]
                }

                # Variations
                for v in p.variations:
                    vtype = v.variation_type.lower()  # normaliza para minúsculo

                    if vtype == "size":
                        item["product"]["sizes"].append({"value": v.value, "quantity": v.quantity})
                    elif vtype == "color":
                        item["product"]["colors"].append({"value": v.value, "quantity": v.quantity})

                product_list.append(item)

            return product_list

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
