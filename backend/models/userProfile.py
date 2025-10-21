from typing import Optional
from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Session
from database import db  # sua instância do SQLAlchemy
from models.user import User  # ajuste o caminho conforme necessário
import uuid

class UserProfile(db.Model):
    __tablename__ = 'profiles'

    user_id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    username = Column(String(150), nullable=False, unique=True)
    full_name = Column(String(200), nullable=False)
    birth_date = Column(Date, nullable=False)
    avatar_url = Column(String(255), nullable=True)

    # Relacionamento com User para acessar dados do usuário
    user = relationship('User', back_populates='profile', uselist=False)

    def __init__(self, user_id: int, username: str, full_name: str,
                 birth_date: date, avatar_url: Optional[str] = None):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.birth_date = birth_date
        self.avatar_url = avatar_url


# No model User, ajuste o relacionamento assim:
# class User(db.Model):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     name = Column(String, nullable=False)
#     birth_date = Column(Date, nullable=False)
#
#     profile = relationship('UserProfile', back_populates='user', uselist=False)


def get_user_profile_by_user_id(session: Session, user_id: int) -> Optional[UserProfile]:
    try:
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        if user_id <= 0:
            raise ValueError("ID de usuário inválido")

        # Consulta UserProfile já com relacionamento carregado (join automático)
        profile = session.query(UserProfile).filter_by(user_id=user_id).first()

        if profile:
            # Pode acessar dados relacionados via profile.user.email, profile.user.name etc.
            return profile

        return None

    except Exception as e:
        print(f"Erro ao buscar perfil: {e}")
        raise
