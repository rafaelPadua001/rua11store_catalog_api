from flask import Blueprint, request, jsonify, make_response, redirect
from services.melhorEnvioService import MelhorEnvioService
import os;
from flask_cors import cross_origin
import requests

melhorenvio_bp = Blueprint('melhorEnvio', __name__)
melhor_envio = MelhorEnvioService()

@melhorenvio_bp.route('/login/')
def login_melhor_envio():
    client_id = os.getenv("MELHOR_ENVIO_CLIENT_ID")
    redirect_uri = os.getenv("MELHOR_ENVIO_REDIRECT_URI")
    authorize_url = (
        f"https://www.melhorenvio.com.br/oauth/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
    )
    return redirect(authorize_url)


@melhorenvio_bp.route('/callback')
def melhor_envio_callback():
    code = request.args.get("code")
    if not code:
        return jsonify({'error': 'Código de autorização não recebido'}), 400
    
    client_id = os.getenv("MELHOR_ENVIO_CLIENT_ID")
    client_secret = os.getenv("MELHOR_ENVIO_CLIENT_SECRET")
    redirect_uri = os.getenv("MELHOR_ENVIO_REDIRECT_URI")
    
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }

    token_url = "https://www.melhorenvio.com.br/oauth/token"
    response = requests.post(token_url, data=data, headers={"Accept": "application/json"})

    if response.status_code == 200:  # corrigido typo: status_code
        token_data = response.json()
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']

        # Salvar token no arquivo .env (append com a chave e o valor)
        with open(".env", "a") as env_file:
            env_file.write(f"\nMELHOR_ENVIO_TOKEN={access_token}\n")
            env_file.write(f"MELHOR_ENVIO_REFRESH_TOKEN={refresh_token}\n")
        
        return jsonify({"message": "Token obtido com sucesso!", "token": access_token})
    else:
        return jsonify({"error": "Falha ao obter token", "details": response.text}), response.status_code

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
    
    try:
        service = MelhorEnvioService()
        result, status_code = service.checkout_shipment(data)
        return jsonify(result), status_code
    except Exception as e:
        print('Error', str(e))
        return jsonify({"error": "Erro ao consultar item"}), 500
    

@melhorenvio_bp.route('/shipmentPrint', methods=['POST'])
def shipment_print():
    data = request.get_json()
    service = MelhorEnvioService()
    response = service.print_label(data)  # retorna só um dict

    # Retorna JSON com status 200 OK
    return jsonify(response), 200


@melhorenvio_bp.route('/shipmentGenerate', methods=["POST"])
def shipmentGenerate():
    data = request.get_json()

    try:
        service = MelhorEnvioService()
        result = service.generate_label(data)
        return jsonify(result), 200
    except Exception as e:
        print('Error', str(e))
        return jsonify({"error": "Erro ao gerar remessa"}), 500
    
@melhorenvio_bp.route('/pdfTag', methods=["POST"])
def pdf_tag_route():
    data = request.get_json(force=True)
    service = MelhorEnvioService()  
    return service.pdfTag(data)   

@melhorenvio_bp.route('/shipmentTracking', methods=["POST"])
def shipmentTracking():
    data = request.get_json()
    print(data)
    try:
        service = MelhorEnvioService()
        result = service.tracking(data)
        return jsonify(result), 200
    except Exception as e:
        print("Error", str(e))
        return jsonify({'error': 'Error ao fazer tracking'})

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


    
