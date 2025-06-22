from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, desc
from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import UUID
from database import db  # Supondo que você tenha Base e engine já configurados no db.py
import uuid


class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    delivery_id = Column(Integer, ForeignKey('delivery.id'))
    shipment_info = Column(Text, nullable=True)
    total_amount = Column(Float, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=True)

    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    #product = relationship('Product') 
    delivery = db.relationship('Delivery', primaryjoin="Order.id==foreign(Delivery.order_id)", backref='order', uselist=False)
    payment = relationship('Payment', back_populates='orders', uselist=False)
    



    # order_items = relationship('OrderItem', back_populates='order')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "payment_id": self.payment_id,
            "delivery_id": self.delivery_id,
            "shipment_info": self.shipment_info,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "status": self.status,
            "total_amount": self.total_amount,
            'products': [
                {
                    'name': item.product.name,
                    'description': item.product.description,
                    'quantity': item.quantity,
                    'unit_price': item.product.price,
                    'total_price': item.total_price
                }
                for item in self.items if item.product  # Para garantir que o relacionamento existe
            ]
        }

    @staticmethod
    def get_all():
        orders = db.session.query(Order).order_by(Order.id.desc()).all()
        return [order.to_dict() for order in orders]

    
    @staticmethod
    def get_by_user_id(user_id):
        try:
            user_uuid = UUID(user_id)  # converter para UUID, se necessário
        except ValueError:
            return None

        orders = (
            db.session.query(Order)
            .filter(Order.user_id == user_uuid)
            .order_by(desc(Order.id))
            .all()
        )
        return [order.to_dict() for order in orders]



    def save(self, session: Session):
        try:
            session.add(self)
            session.commit()
            return self.id
        except Exception as e:
            session.rollback()
            raise Exception(f"Erro ao salvar o pedido: {str(e)}")


