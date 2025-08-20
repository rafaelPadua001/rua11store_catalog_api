from datetime import datetime
from models.couponUser import CouponUser
from database import db
import uuid

class CouponUserController:
    def __init__(self):
        self.db_session = db.session

    def normalize_uuid(self, value):
        if not value:
            return None
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(str(value))

    def create_user_coupon(self, coupon_id, client_id, client_username,
                           title, code, discount, start_date, end_date,
                           created_at, updated_at):

        client_id_uuid = self.normalize_uuid(client_id)
        discount = float(discount)

        existing = self.db_session.query(CouponUser).filter_by(code=code).first()
        if existing:
            raise Exception("Já existe um cupom com esse código.")

        new_user_coupon = CouponUser(
            coupon_id=coupon_id,
            client_id=client_id_uuid,
            client_username=client_username,
            title=title,
            code=code,
            discount=discount,
            start_date=start_date,
            end_date=end_date,
            created_at=created_at,
            updated_at=updated_at
        )

        self.db_session.add(new_user_coupon)
        self.db_session.commit()
        return new_user_coupon.to_dict()

    def update_user_coupon(self, coupon_id, client_id=None,
                           client_username=None, title=None, code=None,
                           discount=None, start_date=None, end_date=None):

        coupon_user = self.db_session.query(CouponUser).filter_by(coupon_id=coupon_id).first()
        if not coupon_user:
            return None

        if client_id is not None:
            coupon_user.client_id = self.normalize_uuid(client_id)
        if client_username is not None:
            coupon_user.client_username = client_username
        if title is not None:
            coupon_user.title = title
        if code is not None:
            coupon_user.code = code
        if discount is not None:
            coupon_user.discount = float(discount)
        if start_date is not None:
            coupon_user.start_date = start_date
        if end_date is not None:
            coupon_user.end_date = end_date

        coupon_user.updated_at = datetime.utcnow()
        self.db_session.commit()
        return coupon_user.to_dict()

    def delete_user_coupon(self, coupon_id):
        coupon_users = self.db_session.query(CouponUser).filter_by(coupon_id=coupon_id).all()
        for coupon in coupon_users:
            self.db_session.delete(coupon)
        self.db_session.commit()
        return True
