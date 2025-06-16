from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import db  # ou o local correto da sua instância SQLAlchemy
from models.order import Order
from models.orderItem import OrderItem
from models.product import Product
class Delivery(db.Model):
    __tablename__ = 'delivery'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=False)
    recipient_name = Column(String(255))
    street = Column(String(255))
    number = Column(String(50))
    complement = Column(String(255))
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    country = Column(String(100))
    phone = Column(String(20))
    bairro = Column(String(100))
    total_value = Column(Float)
    delivery_id = Column(String(100))
    width = Column(Float)
    height = Column(Float)
    length = Column(Float)
    weight = Column(Float)
    cpf = Column(String(20))
    melhorenvio_id = Column(String(100), unique=True)
    order_id = Column(Integer, ForeignKey('orders.id'))

    order = relationship('Order', back_populates='delivery')

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "recipient_name": self.recipient_name,
            "street": self.street,
            "number": self.number,
            "complement": self.complement,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
            "phone": self.phone,
            "bairro": self.bairro,
            "total_value": self.total_value,
            "delivery_id": self.delivery_id,
            "width": self.width,
            "height": self.height,
            "length": self.length,
            "weight": self.weight,
            "cpf": self.cpf,
            "melhorenvio_id": self.melhorenvio_id,
            "order_id": self.order_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update_shipment(shipment_data):
        try:
            delivery = Delivery.query.filter_by(melhorenvio_id=shipment_data['melhorenvio_id']).first()
            if not delivery:
                return False

            delivery.status = shipment_data['status']
            delivery.service_status = shipment_data['service_status']
            delivery.state_abbr = shipment_data['state_abbr']
            delivery.company_name = shipment_data['company_name']
            delivery.tracking_link = shipment_data['tracking_link']

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar entrega: {e}")
            return False

    @staticmethod
    def get_all():
     
        from models.payment import Payment

        deliveries = Delivery.query \
            .join(Order, Delivery.id == Order.delivery_id) \
            .outerjoin(OrderItem, Order.id == OrderItem.order_id) \
            .outerjoin(Product, OrderItem.product_id == Product.id) \
            .outerjoin(Payment, Order.payment_id == Payment.id) \
            .order_by(Delivery.id.desc()).all()

        deliveries_dict = {}

        for d in deliveries:
            if d.id not in deliveries_dict:
                deliveries_dict[d.id] = {
                    'id': d.id,
                    'recipient_name': d.recipient_name,
                    'street': d.street,
                    'number': d.number,
                    'complement': d.complement,
                    'city': d.city,
                    'state': d.state,
                    'zip_code': d.zip_code,
                    'country': d.country,
                    'phone': d.phone,
                    'bairro': d.bairro,
                    'total_value': d.total_value,
                    'width': d.width,
                    'height': d.height,
                    'length': d.length,
                    'weight': d.weight,
                    'melhorenvio_id': d.melhorenvio_id,
                    'order_id': d.order.id if d.order else None,
                    'user_id': d.order.user_id if d.order else None,
                    'payment_id': d.order.payment_id if d.order else None,
                    'cpf': d.order.payment.cpf if d.order and d.order.payment else None,
                    'email': d.order.payment.email if d.order and d.order.payment else None,
                    'order_total': d.order.total_amount if d.order else None,
                    'order_date': d.order.order_date if d.order else None,
                    'status': d.order.status if d.order else None,
                    'products': []
                }

            if d.order and d.order.items:
                for item in d.order.items:
                    deliveries_dict[d.id]['products'].append({
                        'product_id': item.product_id,
                        'name': item.product.name if item.product else None,
                        'description': item.product.description if item.product else None,
                        'image': item.product.image_path if item.product else None,
                        'price': item.unit_price,
                        'quantity': item.quantity
                    })

        return list(deliveries_dict.values())
