from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from extensions import socketio
from controllers.stockController import StockController
from flask import session
from utils.notifications_utils import create_notification
from services.fcm_service import send_fcm_notification
import requests
import os
import uuid
import extensions
from models.delivery import Delivery # se você tiver essa model
from models.order import Order
from models.user import User
from database import db 
from models.orderItem import OrderItem
from models.paymentProduct import PaymentProduct
from sqlalchemy.dialects.postgresql import UUID
import uuid

connected_users = {}

def trigger_push_notification(order_id, recipient_name, total_value):
        try:
            send_fcm_notification(
                title="📦 Novo Pedido!",
                body=f"Pedido #{order_id} para {recipient_name} - R${total_value:.2f}",
                data={"order_id": str(order_id)}
            )
        except Exception as e:
            print(f"Erro ao enviar push notification: {e}")


class Payment(db.Model):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(String, unique=True, nullable=False) 
    total_value = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_type = Column(String)
    cpf = Column(String)
    email = Column(String)
    name = Column(String)
    status = Column(String)
    usuario_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    coupon_code = Column(String, nullable=True)
    coupon_amount = Column(Float, nullable=True)

    # Relacionamentos (opcional)
    orders = relationship('Order', back_populates='payment')


    def __init__(self,  payment_id, total_value, payment_date, payment_type,
                 cpf, name, email, status, usuario_id, products,
                 address=None, coupon_code=None, coupon_amount=None):
        self.payment_id = payment_id
        self.total_value = total_value
        self.payment_date = payment_date or datetime.now()
        self.payment_type = payment_type
        self.cpf = cpf
        self.name = name
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
            'name': self.name,
            'status': self.status,
            'usuario_id': self.usuario_id,
            'coupon_code': self.coupon_code,
            'coupon_amount': self.coupon_amount
        }
    
    

    def save(self):
        try:
            db.session.add(self)
            db.session.flush()

            payment_id = self.id
            delivery_id = None

            products_list = []
            payload = getattr(self, "payload", {}) or {}
            if isinstance(self.products, dict):
                products_list = self.products.get("items", [])
            elif isinstance(self.products, list):
                products_list = self.products
            else:
                print("⚠ self.products está num formato inesperado:", type(self.products))

            if not products_list:
                return

            total_weight = sum(float(p.get('product_weight', 0)) * int(p.get('quantity', 1)) for p in products_list)
            total_height = sum(float(p.get('product_height', 0)) * int(p.get('quantity', 1)) for p in products_list)
            total_width  = sum(float(p.get('product_width', 0)) * int(p.get('quantity', 1)) for p in products_list)
            total_length = sum(float(p.get('product_length', 0)) * int(p.get('quantity', 1)) for p in products_list)

            
            product_ids = [p['product_id'] for p in products_list]

            
            
            delivery = Delivery(
                product_ids=product_ids,
                user_id=self.usuario_id,
                user_name=self.name,

                recipient_name=(
                    payload.get('recipient_name')                    # vem do payload raiz
                    or self.address.get('recipient_name')         # fallback se um dia vier no endereço
                    or self.name                                  # fallback final
                ),

                street=(
                    self.address.get('street')        # versão interna
                    or self.address.get('logradouro') # versão frontend
                    or None
                ),

                number=(
                    self.address.get('number')
                    or self.address.get('numero')
                    or None
                ),

                complement=(
                    self.address.get('complement')
                    or self.address.get('complemento')
                    or None
                ),

                city=(
                    self.address.get('city')
                    or self.address.get('cidade')
                    or None
                ),

                state=(
                    self.address.get('state')
                    or self.address.get('estado')
                    or None
                ),

                zip_code=(
                    self.address.get('zip_code')
                    or self.address.get('cep')
                    or None
                ),

                country=(
                    self.address.get('country')
                    or self.address.get('pais')
                    or None
                ),

                phone=(
                    self.address.get('phone')
                    or self.address.get('telefone')
                    or None
                ),

                bairro=(
                    self.address.get('bairro')
                    or None
                ),

                total_value=self.address.get('total_value') or payload.get('total'),
                delivery_id=self.address.get('delivery_id') or None,

                width=round(total_width, 2),
                height=round(total_height, 2),
                length=round(total_length, 2),
                weight=round(total_weight, 2)
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

            #print(self.status)
            order = Order(
                user_id=uuid.UUID(str(self.usuario_id)),
                payment_id=payment_id,
                delivery_id=delivery_id,
                shipment_info=(self.address.get('zip_code') or self.address.get('cep') or '') if self.address else '',
                total_amount=self.total_value,
                order_date=datetime.utcnow(),
                status=self.status if hasattr(self, 'status') else 'pendente'
            )
            db.session.add(order)
            db.session.flush()
            order_id = order.id

            admins = User.query.filter_by(type='admin').all()
            message = f"Novo pedido recebido: #{order_id}, Para: {self.address.get('recipient_name', 'Cliente')}, valor total: R${self.total_value:.2f}",

            
            print("admins:", [str(a.id) for a in admins])
            print("connected_users:", connected_users)
            print("socketio inicializado?", bool(socketio))

            for admin in admins:
                user_id = str(admin.id)

                # Salva no banco
                create_notification(
                    user_id=user_id,
                    message=message,
                    is_global=True,
                    session=db.session
                )

                # Se o admin está conectado, envia em tempo real
                sid = connected_users.get(user_id)
                if sid:
                    socketio.emit(
                        f'notification_{user_id}',
                        {
                            'message': message,
                            'order_id': order_id
                        },
                        to=sid
                    )

            products_html = "<ul style='list-style: none; padding: 0;'>"
            for product in self.products:
                if 'id' not in product:
                    print("Erro: 'id' não encontrado no produto:", product)
                    continue

                product_id = product.get('product_id') # or product.get('id') 
                product_name = product.get('name') or product.get('product_name')
                price = float(product.get('price') or product.get('product_price'))
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
                    total_price= payload.get('total')
                )
                db.session.add(order_item)

            try:
                if extensions.email_controller is None:
                    raise Exception("email_controller não está inicializado!")
                # first mail to client
                
                products_html = """
                <table cellpadding="5" cellspacing="0" border="0" style="width:100%; border-collapse: collapse;">
                """
                for p in self.products:
                    image = p.get('image') or p.get('image_url','https://via.placeholder.com/80')
                    name = p.get('name') or p.get('product_name', 'Produto sem nome')
                    price = p.get('price', 0.0)
                    quantity = p.get('quantity', 1)

                    products_html += f"""
                    <tr>
                        <td style="width:90px; text-align:center; vertical-align:middle;">
                            <img src="{image}" alt="{name}" width="80" style="display:block; border-radius:5px;">
                        </td>
                        <td style="vertical-align:middle; font-size:14px;">
                            <b>{name}</b><br>
                            Quantidade: {quantity}<br>
                            R${price:.2f}
                        </td>
                    </tr>
                    """
                products_html += "</table>"


                extensions.email_controller.send_email(
                    subject=f"Rua11Store Confirmação de pedido n°: #{order_id}",
                    recipients=[self.email],
                    body=f"Seu pedido foi recebido com sucesso!",
                        html = f"""
                        <div style="text-align:center; font-size:14px;">
                            <p>
                                Olá! Seu pedido n°: <b>#{order_id}</b><br>
                                Valor total: <b>R${self.total_value:.2f}</b><br>
                                Status do pedido: <b>{self.status}</b><br><br>
                            </p>
                        </div>

                        <p><b>Itens do seu pedido:</b></p>
                        {products_html}
                        <br>

                        <div style="text-align:center; margin: 20px 0;">
                            <a href="https://rua11store-catalog-api-lbp7.onrender.com/order/{order_id}/download" 
                            style="background-color:#4CAF50; color:white; padding:10px 20px; 
                                    text-decoration:none; border-radius:5px; font-weight:bold; display:inline-block;">
                                📄 Baixar PDF
                            </a>
                        </div>

                        <p>
                            Estamos separando seu pedido para envio.<br>
                            Atenciosamente,<br>
                            Rua11Store.
                        </p>
                    """

                )

                # second mail to admin
                products_html_admin = """
                <table cellpadding="5" cellspacing="0" border="0" style="width:100%; border-collapse: collapse;">
                """
                for p in self.products:
                    image = p.get('image') or p.get('image_url','https://via.placeholder.com/80')
                    name = p.get('name') or p.get('product_name', 'Produto sem nome')
                    price = p.get('price', 0.0)
                    quantity = p.get('quantity', 1)

                    products_html_admin += f"""
                    <tr>
                        <td style="width:90px; text-align:center; vertical-align:middle;">
                            <img src="{image}" alt="{name}" width="80" style="display:block; border-radius:5px;">
                        </td>
                        <td style="vertical-align:middle; font-size:14px;">
                            <b>{name}</b><br>
                            Quantidade: {quantity}<br>
                            R${price:.2f}
                        </td>
                    </tr>
                    """
                products_html_admin += "</table>"

                # Envia e-mail para o admin
                admin_email = os.getenv('SENDER_EMAIL')
                if admin_email:
                    extensions.email_controller.send_email(
                        subject=f"[Alerta de novo pedido] Pedido n°: #{order_id}",
                        recipients=[admin_email],
                        body=f"Novo pedido recebido: #{order_id}, Para: {self.address.get('recipient_name', 'Cliente')}, valor total: R${self.total_value:.2f}",
                        html = f"""
                            <div style="text-align:center; font-size:14px;">
                                <p>
                                    Olá! Um novo pedido foi recebido: <b>#{order_id}</b><br>
                                    Para: <b>{self.address.get('recipient_name', 'Cliente')}</b><br>
                                    Valor total: <b>R${self.total_value:.2f}</b>.<br><br>
                                </p>
                            </div>

                            <p><b>Produtos:</b></p>
                            {products_html_admin}
                            <br>
                            <p>
                                Atenciosamente,<br>
                                Rua11Store.
                            </p>
                        """
                    )

                   
                else:
                    print("Erro: Variável de ambiente SENDER_EMAIL não está definida.")
            except Exception as e:
                print(f'Erro ao enviar e-mail: {e}')

            db.session.commit()

            recipient_name = self.address.get('recipient_name', 'Cliente')
            trigger_push_notification(order_id, recipient_name, self.total_value)
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
