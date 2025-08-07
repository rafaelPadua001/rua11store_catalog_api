from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from database import db  # ou o local correto da sua instância SQLAlchemy
from models.order import Order
from models.orderItem import OrderItem
from models.product import Product


class Delivery(db.Model):
    __tablename__ = 'delivery'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=True)
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
    user_name = Column(String(255))
    serviceid = Column(String(100))
    quote = Column(Float)
    coupon = Column(String(100))
    discount = Column(Float)
    delivery_min = Column(String(100))
    delivery_max = Column(String(100))
    status = Column(String(50))
    diameter = Column(Float)
    format = Column(String(50))
    billed_weight = Column(Float)
    receipt = Column(String(50))
    own_hand = Column(String(50))
    collect = Column(String(50))
    collect_schedule_at = Column(String(100))
    reverse = Column(String(50))
    non_commercial = Column(String(50))
    authorization_code = Column(String(100))  # Corrigido: estava 'authorizathon_code'
    tracking = Column(String(100))
    self_tracking = Column(String(255))
    delivery_receipt = Column(String(255))
    additional_info = Column(String(255))
    cte_key = Column(String(100))
    paid_at = Column(String(100))
    generated_at = Column(String(100))
    posted_at = Column(String(100))
    delivered_at = Column(String(100))
    canceled_at = Column(String(100))
    suspend_at = Column(String(100))
    expired_at = Column(String(100))
    create_at = Column(String(100))
    updated_at = Column(String(100))
    parse_api_at = Column(String(100))
    received_at = Column(String(100))
    risk = Column(String(255))
    #cpf = Column(String(20))
    status = Column(String(50))
    #service_status = Column(String(50))
    #state_abbr = Column(String(10))
    #company_name = Column(String(100))
    #tracking_link = Column(String(255))

    melhorenvio_id = Column(String(100), unique=True)
    order_id = Column(String(100))
    product = relationship('Product', backref=db.backref('deliveries', passive_deletes=True))

    
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
            "width": float(self.width) if self.width is not None else None,
            "height": float(self.height) if self.height is not None else None,
            "length": float(self.length) if self.length is not None else None,
            "weight": float(self.weight) if self.weight is not None else None,
            "user_name": self.user_name,
            "serviceId": self.serviceid,
            "quote": self.quote,
            "coupon": self.coupon,
            "discount": self.discount,
            "delivery_min": self.delivery_min,
            "delivery_max": self.delivery_max,
            "status": self.status,
            "diameter": self.diameter,
            "format": self.format,
            "billed_weight": self.billed_weight,
            "receipt": self.receipt,
            "own_hand": self.own_hand,
            "collect": self.collect,
            "collect_schedule_at": self.collect_schedule_at,
            "reverse": self.reverse,
            "non_commercial": self.non_commercial,
            "authorization_code": self.authorization_code,
            "tracking": self.tracking,
            "self_tracking": self.self_tracking,
            "delivery_receipt": self.delivery_receipt,
            "additional_info": self.additional_info,
            "cte_key": self.cte_key,
            "paid_at": self.paid_at,
            "generated_at": self.generated_at,
            "posted_at": self.posted_at,
            "delivered_at": self.delivered_at,
            "canceled_at": self.canceled_at,
            "suspend_at": self.suspend_at,
            "expired_at": self.expired_at,
            "create_at": self.create_at,
            "updated_at": self.updated_at,
            "parse_api_at": self.parse_api_at,
            "received_at": self.received_at,
            "risk": self.risk,

            #"cpf": self.cpf,
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
        deliveries = Delivery.query.order_by(Delivery.id.desc()).all()

        deliveries_dict = {}

        for d in deliveries:
            print(f"Delivery ID {d.id} - Width: {d.width} | Weight: {d.weight}")
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
                'order_id': d.order_id,  # string, não relacionamento
                'user_id': None,
                'payment_id': None,
                'cpf': None,
                'email': None,
                'order_total': None,
                'order_date': None,
                'status': None,
                'user_name': d.user_name,
                'serviceId': d.serviceid,
                'quote': d.quote,
                'coupon': d.coupon,
                'discount': d.discount,
                'delivery_min': d.delivery_min,
                'delivery_max': d.delivery_max,
                'diameter': d.diameter,
                'format': d.format,
                'billed_weight': d.billed_weight,
                'receipt': d.receipt,
                'own_hand': d.own_hand,
                'collect': d.collect,
                'collect_schedule_at': d.collect_schedule_at,
                'reverse': d.reverse,
                'non_commercial': d.non_commercial,
                'authorization_code': d.authorization_code,
                'tracking': d.tracking,
                'self_tracking': d.self_tracking,
                'delivery_receipt': d.delivery_receipt,
                'additional_info': d.additional_info,
                'cte_key': d.cte_key,
                'paid_at': d.paid_at.isoformat() if d.paid_at else None,
                'generated_at': d.generated_at.isoformat() if d.generated_at else None,
                'posted_at': d.posted_at.isoformat() if d.posted_at else None,
                'delivered_at': d.delivered_at.isoformat() if d.delivered_at else None,
                'canceled_at': d.canceled_at.isoformat() if d.canceled_at else None,
                'suspend_at': d.suspend_at.isoformat() if d.suspend_at else None,
                'expired_at': d.expired_at.isoformat() if d.expired_at else None,
                'create_at': d.create_at.isoformat() if d.create_at else None,
                'updated_at': d.updated_at.isoformat() if d.updated_at else None,
                'parse_api_at': d.parse_api_at.isoformat() if d.parse_api_at else None,
                'received_at': d.received_at.isoformat() if d.received_at else None,
                'risk': d.risk,

                'products': [],
                'orders': []  # <<< ESSENCIAL
            }

            orders = Order.query.filter(Order.delivery_id == d.id).options(db.joinedload(Order.payment)).all()

            # Se houver pedidos, pega o primeiro para preencher os campos principais da entrega
            if orders:
                first_order = orders[0]
                deliveries_dict[d.id]['user_id'] = first_order.user_id
                deliveries_dict[d.id]['payment_id'] = first_order.payment_id
                deliveries_dict[d.id]['cpf'] = first_order.payment.cpf if first_order.payment else None
                deliveries_dict[d.id]['email'] = first_order.payment.email if first_order.payment else None
                deliveries_dict[d.id]['order_total'] = first_order.total_amount
                deliveries_dict[d.id]['order_date'] = first_order.order_date.isoformat() if first_order.order_date else None
                deliveries_dict[d.id]['status'] = first_order.status

            for order in orders:
                order_data = {
                    'order_id': order.id,
                    'user_id': order.user_id,
                    'payment_id': order.payment_id,
                    'order_total': order.total_amount,
                    'order_date': order.order_date.isoformat() if order.order_date else None,
                    'cpf': order.payment.cpf if order.payment else None,
                    'email': order.payment.email if order.payment else None,
                    'status': order.status,
                    'products': []
                }

                for item in order.items:
                    order_data['products'].append({
                        'product_id': item.product_id,
                        'name': item.product.name if item.product else None,
                        'description': item.product.description if item.product else None,
                        'image': item.product.thumbnail_path if item.product else None,
                        'price': item.unit_price,
                        'quantity': item.quantity
                    })

                deliveries_dict[d.id]['orders'].append(order_data)

        return list(deliveries_dict.values())
