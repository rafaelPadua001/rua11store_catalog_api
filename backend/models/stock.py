from datetime import datetime
from database import db
from sqlalchemy.orm import joinedload


class Stock(db.Model):
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key=True)
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_quantity = db.Column(db.Float, nullable=False)
    variations = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = db.relationship('Product', backref=db.backref('stocks', lazy=True))

    def __init__(self, id_product, user_id, category_id, product_name, product_price, product_quantity, variations=None):
        self.id_product = id_product
        self.user_id = user_id
        self.category_id = category_id
        self.product_name = product_name
        self.product_price = product_price
        self.product_quantity = product_quantity
        self.variations = variations
        
    def to_dict(self):
        return {
            "id": self.id,
            "id_product": self.id_product,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "product_quantity": self.product_quantity,
            
            # "product_width": self.product_width,
            # "product_height": self.product_height,
            # "product_weight": self.product_weight,
            # "product_lenght": self.product_lenght,
            "variations": self.variations,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "product": self.product.to_dict() if self.product else None
        }
    
    @classmethod
    def create(cls, data):
        stock = cls(**data)
        db.session.add(stock)
        db.session.commit()
        return stock.id

    @classmethod
    def get_all(cls):
        return cls.query.options(joinedload(cls.product)).all()

    @classmethod
    def get_by_id(cls, stock_id):
        return cls.query.get(stock_id)

    @classmethod
    def get_stock_id_by_product(cls, id_product):
        stock = cls.query.filter_by(id_product=id_product).first()
        return stock.id if stock else None

    @classmethod
    def update(cls, stock_id, data):
        stock = cls.query.get(stock_id)
        if not stock:
            return False
        for key, value in data.items():
            setattr(stock, key, value)
        stock.updated_at = datetime.utcnow()
        db.session.commit()
        return True

    @classmethod
    def update_stock_quantity(cls, product_id, quantity):
        stock = cls.query.filter_by(id_product=product_id).first()
        if not stock:
            return False

        new_quantity = stock.product_quantity - quantity
        if new_quantity < 0:
            return {"error": "Quantidade insuficiente em estoque"}

        old_quantity = stock.product_quantity
        stock.product_quantity = new_quantity
        db.session.commit()
        return {
            "stock_id": stock.id,
            "old_quantity": old_quantity,
            "new_quantity": new_quantity
        }

    @classmethod
    def delete(cls, stock_id):
        stock = cls.query.get(stock_id)
        if not stock:
            return False
        db.session.delete(stock)
        db.session.commit()
        return True

    @classmethod
    def delete_by_productId(cls, product_id):
        stock = cls.query.filter_by(id_product=product_id).first()
        if not stock:
            return False
        db.session.delete(stock)
        db.session.commit()
        return True
