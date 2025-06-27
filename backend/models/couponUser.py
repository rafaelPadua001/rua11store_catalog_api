from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import db  # Supondo que você tenha um arquivo database.py com a Base do SQLAlchemy

class CouponUser(db.Model):
    __tablename__ = 'coupons_user'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    coupon_id = Column(Integer, ForeignKey('coupons.id'), nullable=False)
    
    title = Column(String(255), nullable=False)
    code = Column(String(100), nullable=False)
    discount = Column(Float, nullable=False)
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)

    # Relacionamento com o cupom
    coupon = relationship("Coupon", backref="coupon_users")

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'coupon_id': self.coupon_id,
            'title': self.title,
            'code': self.code,
            'discount': self.discount,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
