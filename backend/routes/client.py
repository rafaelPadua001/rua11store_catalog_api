from flask import Blueprint, request
from controllers.clientUserController import ClientUserController

client_bp = Blueprint("client", __name__, url_prefix="/client")

@client_bp.route("/registerClient", methods=["POST"])
def register_client():
    data = request.get_json()
    return ClientUserController.register_client_controller(data)

@client_bp.route("/loginClient", methods=['POST'])
def login_client():
    data = request.get_json()
    return ClientUserController.login_client_controller(data)

@client_bp.route("/logoutClient", methods=["POST"])
def logout_client():
    return ClientUserController.logout_client_controller()

