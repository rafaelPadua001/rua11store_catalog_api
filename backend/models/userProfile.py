from typing import Optional
from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Session
from database import db # sua instância do SQLAlchemy


class UserProfile:
    def __init__(self, user_id: int, username: str, full_name: str,
                 birth_date: date, email: str,
                 avatar_url: Optional[str] = None,
                 name: Optional[str] = None):
        """
        Inicializa um perfil de usuário completo.

        Args:
            user_id: ID do usuário
            username: Nome de usuário único
            full_name: Nome completo
            birth_date: Data de nascimento (datetime.date)
            email: Endereço de email (obrigatório)
            avatar_url: URL da foto de perfil
            name: Nome alternativo (se diferente de full_name)
        """
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.birth_date = birth_date
        self.email = email
        self.avatar_url = avatar_url
        self.name = name if name else full_name

def get_user_profile_by_user_id(session: Session, user_id) -> Optional[UserProfile]:
    try:
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("ID de usuário inválido")

        # Query com join entre Profile e User
        result = session.query(ProfileModel, UserModel).join(UserModel, ProfileModel.user_id == UserModel.id)\
            .filter(ProfileModel.user_id == user_id).first()

        if result:
            profile, user = result
            return UserProfile(
                user_id=user_id,
                username=profile.username,
                full_name=profile.full_name,
                birth_date=profile.birth_date,
                avatar_url=profile.avatar_url,
                name=user.name,
                email=user.email
            )
        return None

    except Exception as e:
        print(f"Erro ao buscar perfil: {e}")
        raise
