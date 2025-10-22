from flask import Flask, Blueprint, request, jsonify
from controllers.profileController import ProfileController
from database import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/get-profile/<userId>', methods=["GET"])
def get_profile(userId):
    session = db.session
    profile = ProfileController.get_user_profile_by_user_id(session, userId)
    if not profile:
        return {"message": "Perfil não encontrado"}, 404

    email = None
    if profile.client_user:
        email = profile.client_user.email
    elif profile.user:
        email = profile.user.email

    return {
        "id": profile.user_id,
        "username": profile.username,
        "full_name": profile.full_name,
        "email": email,
        "birth_date": profile.birth_date,
        "created_at": profile.created_at,
        
    }


@profile_bp.route('/update-profile/<userId>', methods=["PUT"])
def update_profile(userId):
    return ProfileController.update_profile(userId)