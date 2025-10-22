from flask import request, jsonify
from models.userProfile import UserProfile
from database import db
from sqlalchemy.orm import Session
from typing import Optional



class ProfileController:
    def get_user_profile_by_user_id(session: Session, userId: str) -> Optional[UserProfile]:
        try:
            # Detecta se é string que parece número inteiro
            if isinstance(userId, str) and userId.isdigit():
                filter_value = int(userId)
            else:
                filter_value = userId  # string UUID ou string normal

            profile = session.query(UserProfile).filter_by(user_id=filter_value).first()

            return profile

        except Exception as e:
            print(f"Erro ao buscar perfil: {e}")
            raise




    @staticmethod
    def update_profile(userId):
        data = request.get_json()
        try:
            profile = UserProfile.query.filter_by(user_id=userId).first()
            

            if profile:
                #update user data
                profile.full_name = data.get('full_name', profile.full_name)
          #      profile.email = data.get('email', profile.email)
                profile.phone = data.get('phone', profile.phone)
                profile.mobile = data.get('mobile', profile.mobile)
                #profile.address = data.get('address', profile.address)

            else:
                #create profile
                profile = UserProfile(
                user_id=userId,
                full_name=data.get('full_name'),
                username=data.get('user_name'),
                birth_date=data.get('birth_date'),
                #email=data.get('email'),
                phone=data.get('phone'),
                mobile=data.get('mobile'),
                #address=data.get('address')
            )
            db.session.add(profile)

            db.session.commit()

            return jsonify({
               # "id": profile.id,
                "user_id": profile.user_id,
                "full_name": profile.full_name,
                "username": profile.username,
                "birth_date": profile.birth_date,
              #  "email": profile.email,
                "phone": profile.phone,
                "mobile": profile.mobile,
            #    "address": profile.address
            }), 200
        except Exception as e:
            db.session.rollback()
            print(f"Error ao atualizar perfil {e}")
            return jsonify({"error": str(e)}), 500