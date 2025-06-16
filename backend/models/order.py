from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, Session
from database import db  # Supondo que você tenha Base e engine já configurados no db.py


class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    payment_id = Column(Integer, nullable=True)
    delivery_id = Column(Integer, ForeignKey('delivery.id'), nullable=True)
    shipment_info = Column(Text, nullable=True)
    total_amount = Column(Float, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=True)

    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    delivery = relationship('Delivery', back_populates='order', uselist=False, foreign_keys=[delivery_id])



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
            "items": [item.to_dict() for item in self.items]
        }

    @staticmethod
    def get_all():
        orders = db.session.query(Order).order_by(Order.id.desc()).all()
        return [order.to_dict() for order in orders]

    @staticmethod
    def get_by_user_id(user_id):
        orders = db.session.query(Order).filter_by(user_id=user_id).order_by(Order.id.desc()).all()
        return [order.to_dict() for order in orders] if orders else None

    def save(self, session: Session):
        try:
            session.add(self)
            session.commit()
            return self.id
        except Exception as e:
            session.rollback()
            raise Exception(f"Erro ao salvar o pedido: {str(e)}")


