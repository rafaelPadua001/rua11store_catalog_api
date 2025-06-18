from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, joinedload
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
    #cpf = Column(String(20))
    #status = Column(String(50))
    service_status = Column(String(50))
    state_abbr = Column(String(10))
    company_name = Column(String(100))
    tracking_link = Column(String(255))

    melhorenvio_id = Column(String(100), unique=True)
    order_id = Column(String(100))
  

    
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
                'products': []
            }

            # Aqui você poderia tentar buscar Order se quiser e se fizer sentido
            # mas só funciona se conseguir mapear o d.order_id para o Order.id

            # Exemplo (não vai funcionar se tipos não baterem):
            order = Order.query.filter(Order.delivery_id == d.id).first()
            if order:
                deliveries_dict[d.id]['user_id'] = order.user_id
                deliveries_dict[d.id]['payment_id'] = order.payment_id
                deliveries_dict[d.id]['order_total'] = order.total_amount
                deliveries_dict[d.id]['order_date'] = order.order_date
                
            
                if order.payment:
                    deliveries_dict[d.id]['cpf'] = order.payment.cpf
                    deliveries_dict[d.id]['email'] = order.payment.email
            
                for item in order.items:
                    deliveries_dict[d.id]['products'].append({
                        'product_id': item.product_id,
                        'name': item.product.name if item.product else None,
                        'description': item.product.description if item.product else None,
                        'image': item.product.image_path if item.product else None,
                        'price': item.unit_price,
                        'quantity': item.quantity
                    })

        return list(deliveries_dict.values())
