from models.userProfile import UserProfile
from database import db
from uuid import UUID

class ProfileController:
    @staticmethod
    def get_user_profile_by_user_id(session, user_id):
        try:
            # Tenta converter para UUID; se falhar, deixa como string
            try:
                user_id = str(UUID(str(user_id)))
            except ValueError:
                user_id = str(user_id)  # int antigo convertido para string

            profile = session.query(UserProfile).filter_by(user_id=user_id).first()
            return profile

        except Exception as e:
            print(f"Erro ao buscar perfil: {e}")
            raise
