import os
import requests
import json
import traceback
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import sqlite3
import json
import traceback
from sqlalchemy.orm import Session
from models.delivery import Delivery
from database import db

load_dotenv
import json
from database import db


class MelhorEnvioService:
    def __init__(self):
        self.token = os.environ.get("MELHOR_ENVIO_TOKEN")
        self.baseUrl = "https://sandbox.melhorenvio.com.br/api/v2"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def delivery_calculate(self, zipcode_origin, zipcode_destiny, weight, height, width, length, secure_value=0, quantity=1):
        url = f"{self.baseUrl}/me/shipment/calculate"

        products = [
            {
                "width": width,
                "height": height,
                "length": length,
                "weight": weight,
                "insurance_value": secure_value,
                "quantity": quantity
            }
        ]

        payload = {
            "from": {"postal_code": zipcode_origin},
            "to": {"postal_code": zipcode_destiny},
            "products": products,
            "services": "",
            "options": {
                "receipt": False,
                "own_hand": False,
                "collect": False
            },
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print('Erro ao calcular frete:', e)
            if e.response is not None:
                print("Resposta da API:", e.response.text)

    def create_shipment(self, data, delivery_id=None):
        print(f"Dados recebidos para criar etiqueta: {data}")

        required_fields = [
            "recipient_name", "phone", "email", "zip_code", "street", "number",
            "city", "state", "height", "width", "length", "weight"
        ]

        missing_fields = [field for field in required_fields if field not in data]

        products = data.get("products", [])
        if not products or not all("name" in p and "price" in p and "quantity" in p for p in products):
            missing_fields.append("products válidos (com 'name', 'price', 'quantity')")

        if missing_fields:
            return {"error": f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"}, 400

        if "recipient_type" in data and data["recipient_type"] == "pessoa_juridica":
            cpf_cnpj = data.get("cnpj", "")
            if not self.is_valid_cnpj(cpf_cnpj):
                return {"error": "CNPJ inválido."}, 400
        else:
            cpf_cnpj = data.get("cpf", "")
            if not self.is_valid_cpf(cpf_cnpj):
                return {"error": "CPF inválido."}, 400

        if not cpf_cnpj:
            return {"error": "CPF ou CNPJ do destinatário é obrigatório."}, 400

        shipment_payload = self.build_shipment_payload(data, cpf_cnpj)

        try:
            shipment_data = self.create_shipment_item(shipment_payload)
            shipment_id = shipment_data["id"]
            print(f"ID do envio criado: {shipment_id}")

            # Use a sessão do flask_sqlalchemy aqui
            session = db.session
            try:
                self.update_delivery_with_shipment_id(session, data, shipment_data)
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Erro ao salvar dados no banco: {e}")
                return {"error": "Erro ao salvar dados no banco"}, 500

            return {
                "message": "Envio criado com sucesso. Aguarde pagamento.",
                "shipment": shipment_payload,
                "shipment_id": shipment_id
            }, 200

        except requests.exceptions.RequestException as e:
            print(f"Erro ao criar etiqueta: {e}")
            traceback.print_exc()
            return {"error": "Erro ao criar etiquetas", "exception": str(e)}, 500

    def update_delivery_with_shipment_id(self, session, data, shipment_data):
        delivery = session.query(Delivery).filter_by(id=data['id']).first()
        if delivery:
            delivery.melhorenvio_id = shipment_data['id']
            delivery.order_id = shipment_data['protocol']
            print(f"Delivery ID {data['id']} atualizado com melhorenvio_id {shipment_data['id']} e order_id {shipment_data['protocol']}")
            return True
        else:
            print(f"Delivery com id {data['id']} não encontrado.")
            return False
    # A função execute_query, get_db_connection, etc. foram removidas pois não são necessárias com SQLAlchemy
    def is_valid_cpf(self, cpf):
        # Lógica simples para validar CPF (pode ser melhorado)
        if len(cpf) != 11 or not cpf.isdigit():
            return False
        return True  # Pode adicionar a verificação do algoritmo de CPF aqui

    def is_valid_cnpj(self, cnpj):
        # Lógica simples para validar CNPJ (pode ser melhorado)
        if len(cnpj) != 14 or not cnpj.isdigit():
            return False
        return True  # Pode adicionar a verificação do algoritmo de CNPJ aqui

    def build_shipment_payload(self, data, cpf_cnpj):
        return {
            "service": "2",
            "from": {
                "name": os.getenv("SENDER_NAME"),
                "phone": os.getenv("SENDER_PHONE"),
                "email": os.getenv("SENDER_EMAIL"),
                "postal_code": os.getenv("SENDER_POSTAL_CODE"),
                "address": os.getenv("SENDER_ADDRESS"),
                "number": os.getenv("SENDER_NUMBER"),
                "city": os.getenv("SENDER_CITY"),
                "state_abbr": os.getenv("DF")
            },
            "to": {
                "name": data["recipient_name"],
                "phone": data["phone"],
                "email": data["email"],
                "postal_code": data["zip_code"],
                "address": data["street"],
                "number": data["number"],
                "city": data["city"],
                "state_abbr": data["state"],
                "document": str(cpf_cnpj) if cpf_cnpj else ""
            },
            "products": [
                {
                    "name": p["name"],
                    "quantity": p.get("quantity", 1),
                    "unitary_value": p["price"]
                }
                for p in data.get("products", []) if "name" in p and "price" in p
            ],
            "volumes": [{
                "height": data["height"],
                "width": data["width"],
                "length": data["length"],
                "weight": data["weight"]
            }]
        }

    def make_request(self, url, method, payload=None):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": f"{os.getenv("SENDER_NAME")} ({os.getenv("SENDER_EMAIL")})"
        }
        try:
            if method.lower() == "post":
                response = requests.post(url, headers=headers, json=payload)
            elif method.lower() == "get":
                response = requests.get(url, headers=headers)
            elif method.lower() == "delete":
                response = requests.delete(url, headers=headers, json=payload)
            else:
                raise ValueError("Método HTTP não suportado")

            if response.status_code in [200, 201, 204]:
                if response.status_code == 204:
                    return None, {"status": "success"}

                if response.text.strip():
                    try:
                        return response.json()
                    except ValueError:
                        return None
                else:
                    return None
            else:
                print(f"Erro na requisição: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None

    def create_shipment_item(self, shipment_payload):
        url = f"{self.baseUrl}/me/cart"
        return self.make_request(url, "post", shipment_payload)

    def checkout_cart(self):
        url = f"{self.baseUrl}/cart/checkout"
        return self.make_request(url, "post")

    def checkout_shipment(self, data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return {"status": "error", "message": "JSON inválido"}, 400

        melhorenvio_id = data.get('item', {}).get('melhorenvio_id')

        if not melhorenvio_id:
            return {"status": "error", "message": "order_id ausente"}, 400

        url = f"{self.baseUrl}/me/shipment/checkout"
        payload = {"orders": [melhorenvio_id]}
        item_data = self.make_request(url, "post", payload)

        if item_data:
            return {"status": "success", "data": item_data}, 200
        else:
            return {"status": "not_found"}, 404

    def generate_label(self, data):
        melhorenvio_id = data.get('melhorenvio_id')
        if not melhorenvio_id:
            return {"error": "melhorenvio_id não informado"}, 400

        url = f"{self.baseUrl}/me/shipment/generate"
        payload = {"orders": [melhorenvio_id]}

        response = self.make_request(url, "post", payload)
        
        # Exemplo: espera-se que response seja um dict
        # com a chave "url" contendo o link para o PDF da etiqueta
        if "url" in response:
            pdf_url = response["url"]

            # Baixa o PDF da URL
            pdf_response = requests.get(pdf_url)
            if pdf_response.status_code == 200 and 'application/pdf' in pdf_response.headers.get('Content-Type', ''):
                return pdf_response.content, 200
            else:
                return None, pdf_response.status_code
        else:
            # Pode conter erro na resposta
            return None, 500



    def print_label(self, data):
        melhorenvio_id = data.get('melhorenvio_id')
        if not melhorenvio_id:
            return {"error": "melhorenvio_id não informado"}, 400

        url = f"{self.baseUrl}/me/shipment/print"
        payload = {"orders": [melhorenvio_id]}
        response = self.make_request(url, "post", payload)
        return response

    def checkItemCart(self, data):
        melhorenvio_id = data['melhorenvio_id']
        
        url = f"{self.baseUrl}/me/cart/{melhorenvio_id}"
       
        item_data = self.make_request(url, "get")

        if item_data:
            print('Item encontrado no carrinho:', item_data)
            return {"status": "success", "data": item_data}, 200
        else:
            print('Erro na requisição ou dados não encontrados.')
            return {"status": "not_found"}, 404
    
    def tracking(self, data):
        print(data)
        melhorenvio_id = data.get('order_id')
        if not melhorenvio_id:
            return {"error": "melhorenvio_id não informado"}, 400

        url = f"{self.baseUrl}/me/shipment/tracking"
        payload = {"orders": [melhorenvio_id]}

        response = self.make_request(url, "post", payload)

        return response
    def deleteItemCart(self, data):
        print(data)
        melhorenvio_id = data['melhorenvio_id']
        print(melhorenvio_id)
        url = f"{self.baseUrl}/me/cart/{melhorenvio_id}"

        # Realiza a requisição de delete
        raw_response, response = self.make_request(url, "delete")
        print("Resposta bruta:", raw_response)
        print("Resposta da API:", response)

        # Verifica a resposta da requisição
        if response is None:
            # Caso o retorno seja None (erro na requisição)
            return {"status": "error", "message": "Erro na requisição."}, 500
        
        # Verifica se a resposta contém a chave 'status'
        if response.get("status") == "success":
            print('Item deletado com sucesso.')
            return {"status": "success"}, 204
        elif response.get("status") == "not_found":
            print('Erro: item não encontrado no carrinho.')
            return {"status": "not_found"}, 404
        else:
            print(f'Erro desconhecido: {response}')
            return {"status": "error", "message": "Erro na requisição."}, 500