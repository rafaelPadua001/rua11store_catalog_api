from datetime import datetime
from sqlalchemy.sql.expression import func
from models.coupon import Coupon
from models.couponUser import CouponUser
from controllers.couponUserController import CouponUserController
from controllers.emailController import EmailController
from services.fcm_service import send_fcm_notification, send_notification_to_all_users
from services.cart_service import get_supabase
from flask import jsonify
from database import db  # flask_sqlalchemy.SQLAlchemy instance
import uuid
from flask_mail import Mail

mail = Mail() 

class CouponController:
    def __init__(self):
        # Usar a sessão do Flask-SQLAlchemy direto
        self.db_session = db.session

    def get_all_coupons(self):
        coupons = self.db_session.query(Coupon).all()
        return [
        coupon if hasattr(coupon, 'to_dict') else coupon
        for coupon in coupons
    ]

    def get_coupons_by_user(self, user_id):
        user_coupons = self.db_session.query(CouponUser).filter_by(client_id=user_id).all()
        return [coupon.to_dict() for coupon in user_coupons]
    
    def get_promotional_coupons(self, limit=5):
        now = datetime.utcnow()
        coupons = (
            self.db_session.query(Coupon)
            .filter(Coupon.client_id.is_(None), Coupon.end_date >= now)
            .order_by(func.random())
            .limit(limit)
            .all()
        )
        return [
                coupon if hasattr(coupon, 'to_dict') else coupon
                for coupon in coupons
            ]
    
    def normalize_uuid(self, value):
        if not value:
            return None
        if isinstance(value, uuid.UUID):
            return value
        try:
            return uuid.UUID(str(value))
        except Exception:
            raise ValueError(f"Invalid UUID: {value}")
    
    def create_coupon(self, user_id, client_id, client_username, client_email, title, code, discount, start_date, end_date, image_path=None):
        try:
            user_id = int(user_id)
        except ValueError:
            raise Exception("user_id deve ser um número inteiro.")

        try:
            discount = float(discount)
        except ValueError:
            raise Exception("discount inválido, deve ser número.")

        existing = self.db_session.query(Coupon).filter_by(code=code).first()
        if existing:
            raise Exception("Já existe um cupom com esse código.")

        now = datetime.utcnow()
        client_id_uuid = self.normalize_uuid(client_id)  


        new_coupon = Coupon(
            user_id=user_id,
            client_id=client_id_uuid,
            client_username=client_username,
            title=title,
            code=code,
            discount=discount,
            start_date=start_date,
            end_date=end_date,
            image_path=image_path,
            created_at=now,
            updated_at=now
        )
        self.db_session.add(new_coupon)
        self.db_session.commit()

        if client_id_uuid and client_username:
            user_coupon = CouponUserController()
            user_coupon.create_user_coupon(
                new_coupon.id,
                client_id_uuid,
                client_username,
                title,
                code,
                discount,
                start_date,
                end_date,
                now,
                now
            )

            html_content = f"""
            <p>Olá {client_username},</p>
            <p>Você recebeu um cupom com código <strong>{code}</strong> de desconto de {discount}% válido de {start_date} até {end_date}.</p>
            <p>Aproveite!</p>
            """
            send_mail = EmailController(mail)
            send_mail.send_email(
                subject=f"Você recebeu um novo cupom: {title}",
                recipients=[client_email],
                body=f"Olá {client_username}, você recebeu um novo cupom!",
                html=html_content
            )

             # ----- PUSH NOTIFICATION -----
            try:
                supabase = get_supabase(service=True)
                tokens = (
                    supabase.table("user_devices")
                    .select("device_token")
                    .eq("user_id", client_id_uuid)
                    .execute()
                    .data
                )
                #print(f"[DEBUG] Tokens encontrados para {client_username}: {tokens}? {client_id}")
                for token in tokens:
                    device_token = token.get("device_token")
                    if not device_token:
                        continue

                    send_fcm_notification(
                        token=device_token,
                        title="🎁 Você recebeu um cupom!",
                        body=f"{discount}% OFF com o código {code} válido até {end_date}.",
                        data={"coupon_id": str(new_coupon.id), "code": code},
                        link="https://rua11store-web.vercel.app/coupons"
                    )
                    print(f"📲 Notificação enviada para {client_username}")
            except Exception as e:
                print(f"❌ Erro ao enviar notificação push: {e}")
        else:
            # ----- CUPOM GERAL -----
            try:
                send_notification_to_all_users(
                    title="🎁 Novo cupom disponível!",
                    body=f"Use o código {code} e ganhe {discount}% OFF até {end_date}!",
                    data={"coupon_id": str(new_coupon.id), "code": code},
                    link="https://rua11store-web.vercel.app/coupons"
                )
                print("📢 Notificação enviada para todos os usuários")
            except Exception as e:
                print(f"❌ Erro ao enviar notificação em massa: {e}")    
        return new_coupon.to_dict()


    def update_coupon(self, coupon_id, current_user_id, client_id, title, code, discount, start_date, end_date, image_path=None):
        coupon = self.db_session.query(Coupon).filter_by(id=coupon_id).first()
        if not coupon:
            return None

        # Usa o user_id da sessão atual
        coupon.user_id = current_user_id  # já é int, obtido da sessão Flask
        coupon.client_id = self.normalize_uuid(client_id)  # sempre UUID
        coupon.title = title
        coupon.code = code
        coupon.discount = float(discount)
        coupon.start_date = start_date
        coupon.end_date = end_date
        coupon.image_path = image_path
        coupon.updated_at = datetime.utcnow()

        self.db_session.commit()

        if coupon.client_id and coupon.client_username:
            user_coupon = CouponUserController()
            user_coupon.update_user_coupon(
                coupon_id=coupon_id,
                user_id=current_user_id,
                client_id=self.normalize_uuid(coupon.client_id),
                client_username=coupon.client_username,
                title=title,
                code=code,
                discount=float(discount),
                start_date=start_date,
                end_date=end_date
            )

        return coupon.to_dict()



    def delete_coupon(self, coupon_id):
        coupon = self.db_session.query(Coupon).filter_by(id=coupon_id).first()
        if not coupon:
            return None

        coupon_user = CouponUserController()
        coupon_user.delete_user_coupon(coupon_id)

        self.db_session.delete(coupon)
        self.db_session.commit()
        return coupon.to_dict()

    def delete_coupons_by_client(self, coupon_id, user_id):
        coupon = self.db_session.query(CouponUser).filter_by(id=coupon_id, client_id=user_id).first()
        if not coupon:
            return False

        self.db_session.delete(coupon)
        self.db_session.commit()
        return True

    
    def pick_up_coupon_by_client_id(self, data):
        client_id = data.get('client_id')
        client_username = data.get('client_username')
        coupon_title = data.get('coupon_title')
        
        if not client_id or not coupon_title:
            return {'error': 'client_id e coupon_title são obrigatórios.'}, 400

        coupon = self.db_session.query(Coupon).filter_by(title=coupon_title).first()
        if not coupon:
            return {'error': 'Cupom não encontrado.'}, 404

        existing = self.db_session.query(CouponUser).filter_by(client_id=self.normalize_uuid(client_id), coupon_id=coupon.id).first()

        if existing:
            return existing.to_dict(), 200

        now = datetime.utcnow()
        new_coupon_user = CouponUser(
            client_id=client_id,
            client_username=client_username,
            coupon_id=coupon.id,
            title=coupon.title,
            code=coupon.code,
            discount=coupon.discount,
            start_date=coupon.start_date,
            end_date=coupon.end_date,
            created_at=now
        )
        self.db_session.add(new_coupon_user)
        self.db_session.commit()

        return new_coupon_user.to_dict(), 201
