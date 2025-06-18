from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from extensions import socketio
from controllers.stockController import StockController
from flask import session
from utils.notifications_utils import create_notification
import requests
import os
import uuid
import extensions
from models.delivery import Delivery # se você tiver essa model
from models.order import Order
from database import db 
from models.orderItem import OrderItem
from models.paymentProduct import PaymentProduct
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Payment(db.Model):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(String, unique=True, nullable=False) 
    total_value = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_type = Column(String)
    cpf = Column(String)
    email = Column(String)
    status = Column(String)
    usuario_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    coupon_code = Column(String, nullable=True)
    coupon_amount = Column(Float, nullable=True)

    # Relacionamentos (opcional)
    orders = relationship('Order', back_populates='payment')


    def __init__(self,  payment_id, total_value, payment_date, payment_type,
                 cpf, email, status, usuario_id, products,
                 address=None, coupon_code=None, coupon_amount=None):
        self.payment_id = payment_id
        self.total_value = total_value
        self.payment_date = payment_date or datetime.now()
        self.payment_type = payment_type
        self.cpf = cpf
        self.email = email
        self.status = status
        self.usuario_id = usuario_id
        self.products = products
        self.address = address
        self.coupon_code = coupon_code
        self.coupon_amount = coupon_amount

    @staticmethod
    def get_all_payments():
        payments = Payment.query.order_by(Payment.payment_date.desc()).all()
        return [p.as_dict() for p in payments]

    def as_dict(self):
        return {
            'id': self.id,
            'payment_id': self.payment_id,
            'total_value': self.total_value,
            'payment_date': self.payment_date.isoformat(),
            'payment_type': self.payment_type,
            'cpf': self.cpf,
            'email': self.email,
            'status': self.status,
            'usuario_id': self.usuario_id,
            'coupon_code': self.coupon_code,
            'coupon_amount': self.coupon_amount
        }

    def save(self):
        try:
            db.session.add(self)
            db.session.flush()  # Garante que o pagamento esteja no banco

            payment_id = self.id
            delivery_id = None

          

            if self.address and self.products:
                product = self.products[0]
                delivery = Delivery(
                    product_id=product['product_id'],
                    user_id=self.usuario_id,
                    recipient_name=self.address.get('recipient_name', ''),
                    street=self.address.get('street', ''),
                    number=self.address.get('number', ''),
                    complement=self.address.get('complement', ''),
                    city=self.address.get('city', ''),
                    state=self.address.get('state', ''),
                    zip_code=self.address.get('zip_code', ''),
                    country=self.address.get('country', ''),
                    phone=self.address.get('phone', ''),
                    bairro=self.address.get('bairro', ''),
                    total_value=self.address.get('total_value', 0),
                    delivery_id=self.address.get('delivery_id', ''),
                    width=product.get('width', 0),
                    height=product.get('height', 0),
                    length=product.get('length', 0),
                    weight=product.get('weight', 0)
                )
                db.session.add(delivery)
                db.session.flush()
                delivery_id = delivery.id

            for product in self.products:
                product_id = product.get('id') or product.get('product_id')
                quantity = int(product.get('quantity', 1))
                result = StockController.update_stock_quantity(product_id, quantity)
                if 'error' in result:
                    print(f"Erro ao atualizar o estoque para {product_id}: {result['error']}")

            order = Order(
                user_id=uuid.UUID(str(self.usuario_id)),
                payment_id=payment_id,
                delivery_id=delivery_id,
                shipment_info=self.address.get('zip_code', '') if self.address else '',
                total_amount=self.total_value,
                order_date=datetime.utcnow()
            )
            db.session.add(order)
            db.session.flush()
            order_id = order.id

            create_notification(
                message=f"Novo pedido recebido: #{order_id}, Para: {self.address.get('recipient_name', 'Cliente')}, valor total: R${self.total_value:.2f}",
                is_global=True,
                session=db.session
            )

            socketio.emit('new_notification', {
                'message': f"Novo pedido recebido: #{order_id}, Para: {self.address.get('recipient_name', 'Cliente')}, valor total: R${self.total_value:.2f}",
                'order_id': order_id,
                'is_global': True
            })

            for product in self.products:
                if 'id' not in product:
                    print("Erro: 'id' não encontrado no produto:", product)
                    continue

                product_id = product.get('id') or product.get('product_id')
                product_name = product.get('name') or product.get('product_name')
                price = float(product.get('price', 0))
                quantity = int(product.get('quantity', 1))

                payment_product = PaymentProduct(
                    payment_id=payment_id,
                    product_id=product_id,
                    product_name=product_name,
                    product_quantity=quantity,
                    product_price=price
                )
                db.session.add(payment_product)

                order_item = OrderItem(
                    order_id=order_id,
                    product_id=product_id,
                    quantity=quantity,
                    unit_price=price,
                    total_price=price * quantity
                )
                db.session.add(order_item)

            try:
                if extensions.email_controller is None:
                    raise Exception("email_controller não está inicializado!")
                extensions.email_controller.send_email(
                    subject=f"Rua11Store Confirmação de pedido n°: {order_id}",
                    recipients=[self.email],
                    body="Seu pedido foi recebido com sucesso!",
                    html=f"<p>Olá! Seu pedido n°: <b>{order_id}</b><br>"
                         f"Status do pedido: <b>{self.status}</b><br>"
                         f"Estamos separando seu pedido para envio.<br>"
                         f"Valor total: <b>R${self.total_value:.2f}</b>.<br><br>"
                         f"Atenciosamente,<br>Rua11Store.</p>"
                )
            except Exception as e:
                print(f'Erro ao enviar e-mail: {e}')

            db.session.commit()
        except Exception as e:
            print(f"Erro ao salvar o pagamento: {e}")
            db.session.rollback()

    @staticmethod
    def update_status(payment_id, status):
        try:
            payment = Payment.query.filter_by(payment_id=payment_id).first()
            if payment:
                payment.status = status
                db.session.commit()
                print(f"Status do pagamento {payment_id} atualizado para {status}.")
                return True
            else:
                print(f"Pagamento com ID {payment_id} não encontrado.")
                return False
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
            db.session.rollback()
            return False

    @staticmethod
    def fetch_from_mercado_pago(payment_id, data=None):
        token = os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')
        url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.put(url, headers=headers, json=data) if data else requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Erro {response.status_code}: {response.text}")
        except Exception as e:
            return {"error": str(e)}

    def payment_chargeback_mercado_pago(payment_id):
        token = os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')
        url = f"https://api.mercadopago.com/v1/payments/chargebacks/{payment_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Erro {response.status_code}: {response.text}")
        except Exception as e:
            return {"error": str(e)}

    def refund_payment_mercado_pago(payment_id, data):
        token = os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')
        url = f"https://api.mercadopago.com/v1/payments/{payment_id}/refunds"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Idempotency-Key": str(uuid.uuid4())
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(f"Erro {response.status_code}: {response.text}")
        except Exception as e:
            return {"error": str(e)}
