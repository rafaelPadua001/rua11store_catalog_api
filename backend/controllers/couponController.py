from datetime import datetime
from models.coupon import Coupon
from models.couponUser import CouponUser
from flask import jsonify
from database import db  # flask_sqlalchemy.SQLAlchemy instance


class CouponController:
    def __init__(self):
        # Usar a sessão do Flask-SQLAlchemy direto
        self.db_session = db.session

    def get_all_coupons(self):
        coupons = self.db_session.query(Coupon).all()
        return [coupon.to_dict() for coupon in coupons]

    def get_coupons_by_user(self, user_id):
        user_coupons = self.db_session.query(CouponUser).filter_by(client_id=user_id).all()
        return [coupon.to_dict() for coupon in user_coupons]

    def create_coupon(self, user_id, client_id, title, code, discount, start_date, end_date, image_path=None):
        existing = self.db_session.query(Coupon).filter_by(code=code).first()
        if existing:
            raise Exception("Já existe um cupom com esse código.")

        now = datetime.utcnow()
        new_coupon = Coupon(
            user_id=user_id,
            client_id=client_id,
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
        return new_coupon.to_dict()

    def update_coupon(self, coupon_id, user_id, client_id, title, code, discount, start_date, end_date, image_path=None):
        coupon = self.db_session.query(Coupon).filter_by(id=coupon_id).first()
        if not coupon:
            return None

        coupon.user_id = user_id
        coupon.client_id = client_id
        coupon.title = title
        coupon.code = code
        coupon.discount = discount
        coupon.start_date = start_date
        coupon.end_date = end_date
        coupon.image_path = image_path
        coupon.updated_at = datetime.utcnow()

        self.db_session.commit()
        return coupon.to_dict()

    def delete_coupon(self, coupon_id):
        coupon = self.db_session.query(Coupon).filter_by(id=coupon_id).first()
        if not coupon:
            return None

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
        coupon_title = data.get('coupon_title')

        if not client_id or not coupon_title:
            return {'error': 'client_id e coupon_title são obrigatórios.'}, 400

        coupon = self.db_session.query(Coupon).filter_by(title=coupon_title).first()
        if not coupon:
            return {'error': 'Cupom não encontrado.'}, 404

        existing = self.db_session.query(CouponUser).filter_by(client_id=client_id, coupon_id=coupon.id).first()
        if existing:
            return existing.to_dict(), 200

        now = datetime.utcnow()
        new_coupon_user = CouponUser(
            client_id=client_id,
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
