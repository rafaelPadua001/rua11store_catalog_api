from flask import Blueprint, request, jsonify
from services.melhorEnvioService import MelhorEnvioService
import os;

melhorenvio_bp = Blueprint('melhorEnvio', __name__)
melhor_envio = MelhorEnvioService()

@melhorenvio_bp.route("/calculate-delivery", methods=["POST"])
def calculate_delivery():
    data = request.json
    
    try:
        zipcode_origin = data['zipcode_origin']
        zipcode_destiny = data['zipcode_destiny']
        products = data['products']

        #init values
        total_weight = 0
        total_height = 0
        total_width = 0
        total_length = 0
        total_insurance = 0
        total_quantity = 0

        for product in products:
            total_weight += float(product.get('weight', 0)) * product.get('quantity', 1)
            total_height += float(product.get('height', 0)) * product.get('quantity', 1)
            total_height += float(product.get('height', 0)) * product.get('quantity', 1)
            total_length += float(product.get('length', 1)) * product.get('quantity', 1)
            total_insurance += float(product.get('secure_value', 0)) * product.get('quantity', 1)
            total_quantity += product.get('quantity', 1)

        result = melhor_envio.delivery_calculate(
            zipcode_origin,
            zipcode_destiny,
            total_weight,
            total_height,
            total_width,
            total_length,
            total_insurance,
            total_quantity
        )

        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Não foi possivel caclular o frete"}), 500
        

    except KeyError as e:
        return jsonify({"error": f"Campo obrigatorio faltando {str(e)}"}), 400
    
@melhorenvio_bp.route('/createTag', methods=['POST'])
def crateTag():
    data = request.get_json()

    try:
        service = MelhorEnvioService()
        result, status_code = service.create_tag(data)  # Desempacota a tupla
        return jsonify(result), status_code  # Usa o resultado diretamente

    except Exception as e:
        print('Error', str(e))
        return jsonify({"error": "Erro ao criar etiquetas"}), 500
    
@melhorenvio_bp.route('/checkItemInCart/<int:id>', methods=["POST"])
def checkItemInCart(id):
    data = request.get_json()
    
    try:
        service = MelhorEnvioService()
        result, status_code = service.checkItemCart(data)
        return jsonify(result), status_code
    except Exception as e:
        print('Error', str(e))
        return jsonify({"error": "Erro ao consultar item"}), 500

