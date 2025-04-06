from flask import Blueprint, request, jsonify
from services.melhorEnvioService import MelhorEnvioService
import os;

melhorenvio_bp = Blueprint('melhorenvio', __name__)
melhor_envio = MelhorEnvioService()

@melhorenvio_bp.route("/calculate-delivery", methods=["POST"])
def calculate_delivery():
    data = request.json

    try:
        zipcode_origin = data['zipcode_origin']
        zipcode_destiny = data['zipcode_destiny']
        weight = data['weight']
        height = data['height']
        width = data['width']
        length = data['length']
        insurance_value = float(data.get("secure_value", 0))
        quantity = data['quantity']


        result = melhor_envio.delivery_calculate(
            zipcode_origin,
            zipcode_destiny,
            weight,
            height,
            width,
            length,
            insurance_value,
            quantity
        )

        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Não foi possivel caclular o frete"}), 500
        

    except KeyError as e:
        return jsonify({"error": f"Campo obrigatorio faltando {str(e)}"}), 400
    
