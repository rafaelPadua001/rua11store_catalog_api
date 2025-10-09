import uuid
from sqlalchemy.dialects.postgresql import UUID
from database import db

class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    client_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("client_users.id"), nullable=False)
    
    cep = db.Column(db.String(9), nullable=False)
    logradouro = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    pais = db.Column(db.String(50), default="Brasil")
    referencia = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    client_user = db.relationship("ClientUser", back_populates="addresses")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}