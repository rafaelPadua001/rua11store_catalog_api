from flask import Blueprint, request
from controllers.addressController import AddressController
from flask_jwt_extended import jwt_required, get_jwt_identity

address_bp = Blueprint("address", __name__)

@address_bp.route('/get-address', methods=["GET"])
@jwt_required()
def get_address():
    # passa a identidade do usuário para o controller
    user_id = get_jwt_identity()
    return AddressController.get_address(user_id)

@address_bp.route("/create-address", methods=["POST"])
@jwt_required()
def create_address():
    data = request.json
    user_id = get_jwt_identity()
    return AddressController.create_address()

