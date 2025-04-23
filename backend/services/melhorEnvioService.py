import os
import requests
import sqlite3

class MelhorEnvioService:
    def __init__(self):
        self.token = os.environ.get("MELHOR_ENVIO_TOKEN")
        self.baseUrl = "https://sandbox.melhorenvio.com.br/api/v2"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    def get_db_connection(self):
        """Cria uma nova conexão com o banco de dados"""
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelos nomes
        return conn
    
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
            "from": {
                "postal_code": zipcode_origin
            },
            "to": {
                "postal_code": zipcode_destiny
            },
            "products": products,
            "services": [],  # get all carrier
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

    def create_tag(self, data, delivery_id=None):
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
            # Criando o envio (cart)
            shipment_data = self.create_shipment(shipment_payload)
            shipment_id = shipment_data["id"]
            print(f"ID do envio criado: {shipment_id}")
           
            # Atualizando a tabela 'delivery' com o ID do envio criado
           
            update = self.update_delivery_with_shipment_id(data, shipment_data)

            return {
                "message": "Envio criado com sucesso. Aguarde pagamento.",
                "shipment": shipment_data
            }, 200

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return {"error": "Erro ao criar etiqueta", "exception": str(e)}, 500

    def update_delivery_with_shipment_id(self, data, shipment_data):
        print('Merdaaaa', data['id'], shipment_data)
        # Aqui, você deve escrever a lógica para atualizar a tabela 'delivery'
        # Exemplo: Atualizar as colunas 'melhorenvio_id' e 'order_id'
        
        try:
            # Atualizando no banco de dados (ajuste conforme sua ORM ou método de acesso ao DB)
            query = """
            UPDATE delivery
            SET melhorenvio_id = ?, order_id = ?
            WHERE id = ?
            """
            params = (shipment_data['id'], shipment_data['protocol'], data['id'])

            # Suponha que você tenha um método para executar essa query no seu banco de dados
            self.execute_query(query, params)
            print(f"Delivery ID atualizado com o melhorenvio_id {shipment_data['id']} e order_id {shipment_data['protocol']}")
        except Exception as e:
            print(f"Erro ao atualizar o delivery: {e}")


    def execute_query(self, query, params=None):
        """Executa uma query SQL no banco de dados"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())  # Executa a query com os parâmetros fornecidos
            conn.commit()  # Faz o commit das alterações
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {e}")
            conn.rollback()  # Faz rollback em caso de erro
        finally:
            conn.close()  # Fecha a conexão

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
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            if method.lower() == "post":
                response = requests.post(url, headers=headers, json=payload)
            elif method.lower() == "get":
                response = requests.get(url, headers=headers)
            else:
                raise ValueError("Método HTTP não suportado")

            # Verificando o código de status
            if response.status_code == 200 or response.status_code == 201:
                print(f"Requisição OK ({response.status_code})")
                print("Resposta bruta:", response.text)
                # Verificar se a resposta não está vazia
                if response.text.strip():  # Verifica se o corpo da resposta não é vazio
                    try:
                        return response.json()  # Retorna a resposta como JSON
                    except ValueError as e:
                        print(f"Erro ao tentar converter resposta para JSON: {e}")
                        return None
                else:
                    print("Resposta da API está vazia.")
                    return None
            else:
                print(f"Erro na requisição: {response.status_code} - {response.text}")
                return None  # Retorna None em caso de erro
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return None  # Retorna None em caso de exceção


    def create_shipment(self, shipment_payload):
        url = f"{self.baseUrl}/me/cart"
        return self.make_request(url, "post", shipment_payload)

    def checkout_cart(self):
        url = f"{self.baseUrl}/cart/checkout"
        return self.make_request(url, "post")

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
    
    def checkItemCart(self, data):
        print('Dados recebidos:', data)
        melhorenvio_id = data['melhorenvio_id']

        url = f"{self.baseUrl}/me/cart/{melhorenvio_id}"
        print(url)

        item_data = self.make_request(url, "get")

        if item_data:
            print('Item encontrado no carrinho:', item_data)
            return {"status": "success", "data": item_data}, 200
        else:
            print('Erro na requisição ou dados não encontrados.')
            return {"status": "not_found"}, 404


