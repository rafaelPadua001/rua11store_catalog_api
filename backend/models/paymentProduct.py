from database import db

class PaymentProduct(db.Model):
    __tablename__ = 'payments_product'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.payment_id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    product_price = db.Column(db.Float, nullable=False)

    def __init__(self, payment_id, product_id, product_name, product_quantity, product_price):
        self.payment_id = payment_id
        self.product_id = product_id
        self.product_name = product_name
        self.product_quantity = product_quantity
        self.product_price = product_price
