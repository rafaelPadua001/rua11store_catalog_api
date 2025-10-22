from flask import Blueprint, request
from controllers.clientUserController import ClientUserController
from flask_cors import CORS
from flask_jwt_extended import get_jwt, jwt_required

client_bp = Blueprint("client", __name__, url_prefix="/client")
CORS(client_bp, resources={r"/client/*": {"origins": "*"}}, supports_credentials=True)

@client_bp.route("/registerClient", methods=["POST"])
def register_client():
    data = request.get_json()
    return ClientUserController.register_client_controller(data)

@client_bp.route('/get-logged-client', methods=['GET'])
@jwt_required()
def get_logged_client():
    return ClientUserController.get_logged_client()

@client_bp.route("/get-client", methods=['GET'])
def get_client():
    return ClientUserController.get_client()

@client_bp.route("/loginClient", methods=['POST'])
def login_client():
    data = request.get_json()
    return ClientUserController.login_client_controller(data)

@client_bp.route("/logoutClient", methods=["POST"])
def logout_client():
    return ClientUserController.logout_client_controller()

