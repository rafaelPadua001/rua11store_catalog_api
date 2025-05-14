from flask import Blueprint, request, jsonify
from services.melhorEnvioService import MelhorEnvioService
import os;
from flask_cors import cross_origin

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
    
@melhorenvio_bp.route('/shipmentCreate', methods=['POST'])
def shipmentCreate():
    data = request.get_json()

    try:
        service = MelhorEnvioService()
        result, status_code = service.create_shipment(data)  # Desempacota a tupla
        return jsonify(result), status_code  # Usa o resultado diretamente

    except Exception as e:
        print('Error', str(e))
        return jsonify({"error": "Erro ao criar etiquetas"}), 500
    
@melhorenvio_bp.route('/checkItemInCart/<string:id>', methods=["POST"])
def checkItemInCart(id):
    data = request.get_json()
    
    try:
        service = MelhorEnvioService()
        result, status_code = service.checkItemCart(data)
        return jsonify(result), status_code
    except Exception as e:
        print('Error', str(e))
        return jsonify({"error": "Erro ao consultar item"}), 500
    
@melhorenvio_bp.route('shipmentCheckout', methods=["POST"])
def shipmentCheckout():
    data = request.get_json()
    print('Data', data)
    try:
        service = MelhorEnvioService()
        result, status_code = service.checkout_shipment(data)
        return jsonify(result), status_code
    except Exception as e:
        print('Error', str(e))
        return jsonify({"error": "Erro ao consultar item"}), 500


@melhorenvio_bp.route('/shipmentGenerate', methods=["POST"])
def shipmentGenerate():
    data = request.get_json()

    try:
        service = MelhorEnvioService()
        result, status_code = service.generate_label(data)
        return jsonify(result), status_code
    except Exception as e:
        print('Error', str(e))
        return jsonify({"error": "Erro ao gerar remessa"}), 500
    
@melhorenvio_bp.route('/pdfTag', methods=["POST"])
def payTag():
    data = request.get_json()

    try:
        service = MelhorEnvioService()
        result, status_code = service.pdfTag(data)
        return jsonify(result), status_code
    except Exception as e:
        print('Error', str(e))
        return jsonify({"error": "Erro ao pagar etiqueta"}), 500
    
@melhorenvio_bp.route('/deleteItemCart', methods=["DELETE", "OPTIONS"])
@cross_origin()  # Habilita CORS para essa rota
def deleteItemCart():
    data = request.get_json()

    try:
        print(f"Recebido ID para deleção: {data['melhorenvio_id']}")  # Adiciona log para depuração
        service = MelhorEnvioService()
        result, status_code = service.deleteItemCart(data)

        if status_code == 204:
            # Se o status code for 204, a API foi bem-sucedida mas não há conteúdo a ser retornado
            return jsonify({"status": "success"}), 204
        else:
            # Caso contrário, retorne o resultado como está
            return jsonify(result), status_code
    except Exception as e:
        print('Error', str(e))
        return jsonify({"error": "Erro ao deletar item do carrinho"}), 500


    
