from flask import Flask, Blueprint, request, jsonify
from controllers.profileController import ProfileController
from database import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/get-profile/<uuid:user_id>', methods=["GET"])
def get_profile(user_id):
    print(user_id)
    session = db.session
    profile = ProfileController.get_user_profile_by_user_id(session, user_id)
    if not profile:
        return {"message": "Perfil não encontrado"}, 404
    return {
        "id": profile.user_id,
        "username": profile.username,
        "full_name": profile.full_name,
        "email": profile.user.email
    }