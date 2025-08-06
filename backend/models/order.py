from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, desc
from sqlalchemy.orm import relationship, Session

from database import db  # Supondo que você tenha Base e engine já configurados no db.py
import uuid  


class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(36), nullable=False, default=lambda: str(uuid.uuid4()))
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    delivery_id = Column(Integer, ForeignKey('delivery.id'))
    shipment_info = Column(Text, nullable=True)
    total_amount = Column(Float, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=True)

    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    #product = relationship('Product') 
    delivery = db.relationship('Delivery', backref='orders', uselist=False)

    payment = relationship('Payment', back_populates='orders', uselist=False)
    



    # order_items = relationship('OrderItem', back_populates='order')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "payment_id": self.payment_id,
            "delivery_id": self.delivery_id,
            "melhorenvio_id": self.delivery.melhorenvio_id if self.delivery else None,
            "shipment_info": self.shipment_info,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "status": self.status,
            "total_amount": self.total_amount,
            'products': [
                {
                    'name': item.product.name,
                    'product_image': item.product.thumbnail_path,
                    'description': item.product.description,
                    'quantity': item.quantity,
                    'unit_price': item.product.price,
                    'total_price': item.total_price
                }
                for item in self.items if item.product  # Para garantir que o relacionamento existe
            ],
            'product_seo': [
                {
                    'product_id': item.product.id,
                    'meta_title': item.product.seo.meta_title if item.product and item.product.seo else None,
                    'meta_description': item.product.seo.meta_description if item.product and item.product.seo else None,
                    'keywords': item.product.seo.keywords if item.product and item.product.seo else None,
                    'slug': item.product.seo.slug if item.product and item.product.seo else None,
                }
                for item in self.items if item.product.seo
            ],
           'delivery': 
               {
                'id': self.delivery.id if self.delivery else None,
                'melhorenvio_id': self.delivery.melhorenvio_id if self.delivery else None,
                'order_id': self.delivery.order_id if self.delivery else None,
                'state': self.delivery.state if self.delivery else None,
                'recipient_name': self.delivery.recipient_name if self.delivery else None,
                'street': self.delivery.street if self.delivery else None,
                'number': self.delivery.number if self.delivery else None,
                'complement': self.delivery.complement if self.delivery else None,
                'city': self.delivery.city if self.delivery else None,
                'state': self.delivery.state if self.delivery else None,
                'country': self.delivery.country if self.delivery else None,
                'phone': self.delivery.phone if self.delivery else None,
                'bairro': self.delivery.bairro if self.delivery else None,
                'total_value': self.delivery.total_value if self.delivery else None,
             #   'total': self.delivery.total_value if self.total_value else None,
              #  'created_at': self.delivery.created_at.isoformat() if self.delivery and self.delivery.created_at else None,
                }
           

        }

    @staticmethod
    def get_all():
        orders = db.session.query(Order).order_by(Order.id.desc()).all()
        return [order.to_dict() for order in orders]



    @staticmethod
    def get_by_user_id(user_id):
        print("user_id recebido:", user_id)
        try:
            user_uuid = uuid.UUID(user_id)  # converter para objeto UUID
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


