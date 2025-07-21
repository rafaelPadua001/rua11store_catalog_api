from database import db
from sqlalchemy import Numeric
from sqlalchemy.orm import joinedload
from models.productSeo import ProductSeo


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    price = db.Column(Numeric(10,2))
    category_id = db.Column(db.Integer)
    subcategory_id = db.Column(db.Integer)
    image_path = db.Column(db.String)
    quantity = db.Column(db.Integer, default=1)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    length = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    stock = db.relationship('Stock', back_populates='product', uselist=False)
    seo = db.relationship('ProductSeo', uselist=False, back_populates='product', cascade="all, delete-orphan")

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
            from models.stock import Stock
            from models.productSeo import ProductSeo
            from models.comment import Comment

            results = db.session.query(
                Product,
                Stock.product_quantity,
                ProductSeo,
                Comment
            ).join(
                Stock, Product.id == Stock.id_product
            ).outerjoin(
                ProductSeo, Product.id == ProductSeo.product_id
            ).outerjoin(
                Comment, Product.id == Comment.product_id
            ).all()

            product_map = {}

            for product, quantity, seo, comment in results:
                pid = product.id
                if pid not in product_map:
                   product_map[pid] = {
                    "product": {
                        "id": product.id,
                        "name": product.name,
                        "description": product.description,
                        "price": str(product.price),
                        "image_path": product.image_path,
                        "category_id": product.category_id,
                        "subcategory_id": product.subcategory_id,
                        "user_id": product.user_id,
                        "length": product.length,
                        "width": product.width,
                        "height": product.height,
                        "weight": product.weight,
                        "quantity": product.quantity,
                    },
                    "product_quantity": quantity,
                    "seo": {
                        "meta_title": seo.meta_title if seo else None,
                        "meta_description": seo.meta_description if seo else None,
                        "slug": seo.slug if seo else None,
                        "keywords": seo.keywords if seo else None
                    } if seo else None,
                    "comments": []
                }

                if comment:
                    product_map[pid]["comments"].append({
                        "id": comment.id,
                        "product_id": comment.product_id,
                        "user_id": comment.user_id,
                        "user_name": comment.user_name,
                        "avatar_url": comment.avatar_url,
                        "comment": comment.comment,
                        'status': comment.status,
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
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": f"{self.price:.2f}",
            "category_id": self.category_id,
            "subcategory_id": self.subcategory_id,
            "image_path": self.image_path,
            "quantity": self.quantity,
            "width": self.width,
            "height": self.height,
            "weight": self.weight,
            "length": self.length,
            "user_id": self.user_id,
        }

        if self.seo:  # relacionamento product.seo
            data["seo"] = {
                "meta_title": self.seo.meta_title,
                "meta_description": self.seo.meta_description,
                "slug": self.seo.slug,
                "keywords": self.seo.keywords,
            }
        else:
            data["seo"] = None

        return data

    def to_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'price': self.price,
                'product_quantity': self.quantity,
                'seo': self.seo.to_dict() if self.seo else None,
                'comments': [c.to_dict() for c in self.comments] if self.comments else []
            }