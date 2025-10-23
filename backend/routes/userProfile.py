from flask import Flask, Blueprint, request, jsonify
from controllers.profileController import ProfileController
from models.userProfile import UserProfile
from database import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/get-profile/<userId>', methods=["GET"])
def get_profile(userId):
    session = db.session
    profile = ProfileController.get_user_profile_by_user_id(session, userId)
    
    if not profile:
        return {"message": "Perfil não encontrado"}, 404

    # Se você quer incluir email e name, precisa buscar via session
    email = None
    name = None
    user_obj = session.query(UserProfile).filter_by(user_id=profile["user_id"]).first()
    if user_obj:
        if user_obj.client_user:
            email = user_obj.client_user.email
            name = user_obj.client_user.name
        elif user_obj.user:
            email = user_obj.user.email
            name = user_obj.user.name

    # Acrescenta email e name no dict
    profile["email"] = email
    profile["name"] = name

    return jsonify(profile), 200



@profile_bp.route('/update-profile/<userId>', methods=["PUT"])
def update_profile(userId):
    return ProfileController.update_profile(userId)