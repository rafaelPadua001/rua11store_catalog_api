import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from database import db  # supondo que você já tem db = SQLAlchemy()

class ClientUser(db.Model):
    __tablename__ = "client_users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(150), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), default="client")  # pode ser client/admin/etc
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    addresses = db.relationship("Address", back_populates="client_user")
    
    # setter para salvar senha já criptografada
    @property
    def password(self):
        raise AttributeError("Password não é acessível diretamente")

    @password.setter
    def password(self, plain_password):
        self.password_hash = generate_password_hash(plain_password)

    # checar senha
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
