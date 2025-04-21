from flask import Blueprint, jsonify, request
from models.delivery import Delivery

delivery_bp = Blueprint('delivery', __name__)

@delivery_bp.route('/deliveries', methods=['GET'])
def get_deliveries():
    deliveries = Delivery.get_all()
    return jsonify([d.__dict__ for d in deliveries])

@delivery_bp.route('/deliveries', methods=['POST'])
def create_delivery():
    data = request.get_json()

    required_fields = [
        'user_id', 'product_id', 'recipient_name', 'street', 'number',
        'city', 'state', 'zip_code', 'country'
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Campos opcionais
    complement = data.get('complement', '')
    phone = data.get('phone', '')

    try:
        Delivery.create(
            user_id=data['user_id'],
            product_id=data['product_id'],
            recipient_name=data['recipient_name'],
            street=data['street'],
            number=data['number'],
            complement=complement,
            city=data['city'],
            state=data['state'],
            zip_code=data['zip_code'],
            country=data['country'],
            phone=phone
        )
        return jsonify({"message": "Delivery created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
