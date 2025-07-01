from database import db
from sqlalchemy import Numeric
from sqlalchemy.orm import joinedload


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
            # Faz join de Product com Stock para trazer quantidade
            results = db.session.query(
                Product,
                Stock.product_quantity
            ).join(Stock, Product.id == Stock.id_product).all()

            # results será lista de tuplas (Product, product_quantity)
            products_with_qty = []
            for product, quantity in results:
                # Você pode construir um dict ou objeto conforme precisar
                products_with_qty.append({
                    "product": product,
                    "product_quantity": quantity
                })

            return products_with_qty

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
            "user_id": self.user_id
        }

