from typing import Optional
from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship, Session
from database import db  # sua instância do SQLAlchemy
from models.user import User  # ajuste o caminho conforme necessário
from sqlalchemy import Column, Integer, String, Date, ForeignKey, cast
from sqlalchemy.orm import relationship, Session

class UserProfile(db.Model):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)
    client_user_id = Column(String(36), ForeignKey('client_users.id'), nullable=True, unique=True)

    username = Column(String(150), nullable=False, unique=True)
    full_name = Column(String(200), nullable=False)
    birth_date = Column(Date, nullable=False)
    avatar_url = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    mobile = Column(String(20), nullable=True)

    # Relacionamentos
    user = relationship(
        "User",
        primaryjoin="foreign(cast(User.id, String)) == UserProfile.user_id",
        uselist=False,
        viewonly=True,
    )

    client_user = relationship(
        "ClientUser",
        primaryjoin="foreign(ClientUser.id) == UserProfile.client_user_id",  # corrigido
        uselist=False,
        viewonly=True,
    )



    def __init__(self, user_id: int, username: Optional[str] = None,
             full_name: Optional[str] = None,
             birth_date: Optional[date] = None,
             avatar_url: Optional[str] = None,
             phone: Optional[str] = None,
             mobile: Optional[str] = None):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.birth_date = birth_date
        self.avatar_url = avatar_url
        self.phone = phone
        self.mobile = mobile


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
