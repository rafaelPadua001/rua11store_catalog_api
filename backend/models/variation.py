from database import db
from datetime import datetime

class Variation(db.Model):
    __tablename__ = "product_variations"

    # ID inteiro autoincrementado
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Relacionamento com produto
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    product_name = db.Column(db.String(255), nullable=False)

    variation_type = db.Column(db.String(20), nullable=False)  # "color" ou "size"
    value = db.Column(db.String(255), nullable=False)          # "Vermelho" ou "G"
    quantity = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product", back_populates="variations")
    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "variation_type": self.variation_type,
            "value": self.value,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat(),
        }
