import os
import requests

class MelhorEnvioService:
    def __init__(self):
        self.token = os.environ.get("MELHOR_ENVIO_TOKEN")
        self.baseUrl = "https://sandbox.melhorenvio.com.br/api/v2"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def create_tag(self, data):
        print(f"Dados recebidos para criar etiqueta: {data}")

        # Campos obrigatórios
        required_fields = [
            "recipient_name", "phone", "email", "zip_code", "street", "number",
            "city", "state", "product_name", "product_price", "height", "width", "length", "weight"
        ]
        
        # Verificando se todos os campos obrigatórios estão presentes
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return {"error": f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"}, 400

        # Determinar se o destinatário é pessoa física ou jurídica
        if "recipient_type" in data and data["recipient_type"] == "pessoa_juridica":
            cpf_cnpj = data.get("cnpj", "")
            if not self.is_valid_cnpj(cpf_cnpj):
                return {"error": "CNPJ inválido."}, 400
        else:
            cpf_cnpj = data.get("cpf", "")
            if not self.is_valid_cpf(cpf_cnpj):
                return {"error": "CPF inválido."}, 400

        # Verificando se o CPF ou CNPJ foi enviado corretamente
        if not cpf_cnpj:
            return {"error": "CPF ou CNPJ do destinatário é obrigatório."}, 400

        # Construir o payload do envio
        shipment_payload = self.build_shipment_payload(data, cpf_cnpj)

        try:
            # Criando o envio
            shipment_data = self.create_shipment(shipment_payload)
            shipment_id = shipment_data["id"]
            print(f"ID do envio criado: {shipment_id}")

            # Realizando checkout do envio
            checkout_data = self.checkout_shipment(shipment_id)
            print(f"Dados do checkout: {checkout_data}")

            # Gerando a etiqueta
            generate_data = self.generate_label(shipment_id)
            print(f"Dados da etiqueta gerada: {generate_data}")

            return {
                "shipment": shipment_data,
                "checkout": checkout_data,
                "generate": generate_data
            }, 200

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return {"error": "Erro ao criar etiqueta", "exception": str(e)}, 500

    def build_shipment_payload(self, data, cpf_cnpj):
        # Corrigindo a chave para enviar CPF ou CNPJ
        return {
            "service": "2",  # Exemplo de código do serviço
            "from": {
                "name": "Rua11Store",  # Exemplo de nome do remetente
                "phone": "6199051731",  # Telefone do remetente
                "email": "email@dominio.com",  # Email do remetente
                "postal_code": "73080180",  # CEP do remetente
                "address": "QMS 11",  # Endereço do remetente
                "number": "19",  # Número do endereço do remetente
                "city": "Brasília",  # Cidade do remetente
                "state_abbr": "DF"  # Estado do remetente
            },
            "to": {
                "name": data["recipient_name"],  # Nome do destinatário
                "phone": data["phone"],  # Telefone do destinatário
                "email": data["email"],  # Email do destinatário
                "postal_code": data["zip_code"],  # CEP do destinatário
                "address": data["street"],  # Endereço do destinatário
                "number": data["number"],  # Número do endereço do destinatário
                "city": data["city"],  # Cidade do destinatário
                "state_abbr": data["state"],  # Estado do destinatário
                "document": str(cpf_cnpj) if cpf_cnpj else ""  # Passando o CPF diretamente (como string)
            },
            "products": [{
                "name": data["product_name"],  # Nome do produto
                "quantity": 1,  # Quantidade do produto
                "unitary_value": data["product_price"]  # Preço unitário do produto
            }],
            "volumes": [{
                "height": data["height"],  # Altura do volume
                "width": data["width"],  # Largura do volume
                "length": data["length"],  # Comprimento do volume
                "weight": data["weight"]  # Peso do volume
            }]
        }

    def make_request(self, url, method, payload=None):
        print(f"Enviando requisição {method.upper()} para: {url}")
        response = requests.request(method, url, headers=self.headers, json=payload)
        
        print("Resposta da API:", response.text)
        print("Status:", response.status_code)
        
        if response.status_code != 200:
            print(f"Erro na requisição: {response.text}")
            raise Exception(f"Erro na requisição: {response.text}")
        
        return response.json()

    def create_shipment(self, shipment_payload):
        url = f"{self.baseUrl}/me/cart"
        return self.make_request(url, "post", shipment_payload)

    def checkout_shipment(self, shipment_id):
        url = f"{self.baseUrl}/shipment/checkout"
        return self.make_request(url, "post", {"shipments": [shipment_id]})

    def generate_label(self, shipment_id):
        url = f"{self.baseUrl}/shipment/generate"
        return self.make_request(url, "post", {"shipments": [shipment_id]})

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
