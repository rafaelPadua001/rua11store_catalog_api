from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy.dialects.postgresql as pg
from database import db 
from datetime import datetime


class CouponUser(db.Model):
    __tablename__ = 'coupons_user'

    id = Column(Integer, primary_key=True)
    coupon_id = Column(Integer, ForeignKey('coupons.id'), nullable=False)
    client_id = Column(pg.UUID(as_uuid=True), nullable=False)
    client_username = Column(db.String, nullable=True) 
    title = Column(String(255), nullable=False)
    code = Column(String(100), nullable=False)
    discount = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    # Relacionamento com o cupom
    coupon = relationship("Coupon", backref="coupon_users")

    def to_dict(self):
        def parse_to_iso(date_value):
            if isinstance(date_value, datetime):
                return date_value.isoformat()
            try:
                # Tenta converter de string no formato RFC 2822
                dt = datetime.strptime(date_value, '%a, %d %b %Y %H:%M:%S %Z')
                return dt.isoformat()
            except Exception:
                try:
                    # Tenta converter de string no formato ISO
                    dt = datetime.fromisoformat(date_value)
                    return dt.isoformat()
                except:
                    return str(date_value)  # Retorna como string se falhar

        return {
            'id': self.id,
            'client_id': self.client_id,
            'coupon_id': self.coupon_id,
            'title': self.title,
            'code': self.code,
            'discount': self.discount,
            'start_date': parse_to_iso(self.start_date),
            'end_date': parse_to_iso(self.end_date),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
