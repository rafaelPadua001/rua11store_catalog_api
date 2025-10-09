from flask import Blueprint, request, jsonify
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

@address_bp.route('/update-address/<int:address_id>', methods=["PUT"])
@jwt_required()
def update_address(address_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = AddressController.update_address(user_id, address_id, data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@address_bp.route('/delete-address/<int:address_id>', methods=["DELETE"])
@jwt_required()
def delete_address(address_id):
    user_id = get_jwt_identity()
    return AddressController.delete_address(address_id, user_id)

