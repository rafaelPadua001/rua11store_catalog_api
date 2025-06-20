import os
import requests
import sqlite3
from models.delivery import Delivery
import json
import traceback

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
            "services": "",  # get all carrier
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

        # Campos obrigatórios
        required_fields = [
            "recipient_name", "phone", "email", "zip_code", "street", "number",
            "city", "state", "height", "width", "length", "weight"
        ]

        missing_fields = [field for field in required_fields if field not in data]

        # Verificando se há ao menos um produto válido
        products = data.get("products", [])
        if not products or not all("name" in p and "price" in p and "quantity" in p for p in products):
            missing_fields.append("products válidos (com 'name', 'price', 'quantity')")

        if missing_fields:
            return {"error": f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"}, 400

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
            shipment_data = self.create_shipment_item(shipment_payload)
            shipment_id = shipment_data["id"]
            print(f"ID do envio criado: {shipment_id}")
           
            # Atualizando a tabela 'delivery' com o ID do envio criado
           
            update = self.update_delivery_with_shipment_id(data, shipment_data)

            return {
                "message": "Envio criado com sucesso. Aguarde pagamento.",
                "shipment": shipment_payload,
                "shipment_id": shipment_id
            }, 200

        except requests.exceptions.RequestException as e:
            print(f"Erro ao criar etiqueta: {e}")
            traceback.print_exc()
            return {"error": "Erro ao criar etiquetas", "exception": str(e)}, 500

    def update_delivery_with_shipment_id(self, data, shipment_data):
        
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
            # print(f"Delivery ID atualizado com o melhorenvio_id {shipment_data['id']} e order_id {shipment_data['protocol']}")
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
                "phone": "+556199051731",  # Telefone do remetente
                "email": "rafael.f.p.faria@hotmail.com",  # Email do remetente
                "postal_code": "73082180",  # CEP do remetente
                "address": "QMS 19",  # Endereço do remetente
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
           "products": [
                {
                    "name": p["name"],
                    "quantity": p.get("quantity", 1),
                    "unitary_value": p["price"]
                }
                for p in data.get("products", []) if "name" in p and "price" in p
            ],

            "volumes": [{
                "height": data["height"],  # Altura do volume
                "width": data["width"],  # Largura do volume
                "length": data["length"],  # Comprimento do volume
                "weight": data["weight"]  # Peso do volume
            }]
        }
    
    def make_request(self, url, method, payload=None):
        
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "Rua11Store (rafael.f.p.faria@hotmail.com)"
        }
       
        try:
            # Realiza a requisição de acordo com o método
            if method.lower() == "post":
                response = requests.post(url, headers=headers, json=payload)
            elif method.lower() == "get":
                response = requests.get(url, headers=headers)
            elif method.lower() == "delete":
                response = requests.delete(url, headers=headers, json=payload)
            else:
                raise ValueError("Método HTTP não suportado")

            # Verifica se a resposta tem um status adequado
            if response.status_code in [200, 201, 204]:
                print(f"Requisição OK ({response.status_code})")
                print("Resposta bruta:", response.text)
                
                # Se o status for 204 (sem conteúdo), não há resposta no corpo
                if response.status_code == 204:
                    print("Resposta da API está vazia.")
                    return None, {"status": "success"}  # Retorna um status de sucesso, mesmo sem corpo

                # Verifica se a resposta não está vazia para outros status
                if response.text.strip():  # Verifica se o corpo da resposta não está vazio
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

        except requests.exceptions.RequestException as e:
            # Captura erros de rede ou outros erros da requisição
            print(f"Erro na requisição: {e}")
            return None  # Retorna None em caso de exceção

        except Exception as e:
            # Captura outros erros inesperados
            print(f"Erro inesperado: {e}")
        return None  # Retorna None em caso de exceção genérica
    
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
            print('order_id não encontrado!')
            return {"status": "error", "message": "order_id ausente"}, 400

        url = f"{self.baseUrl}/me/shipment/checkout"
        payload = {"orders": [melhorenvio_id]}
        
        item_data = self.make_request(url, "post", payload)
        print('Resposta da requisição:', item_data)

        if item_data:
            print('Item encontrado no carrinho:', item_data)
            return {"status": "success", "data": item_data}, 200
        else:
            print('Erro na requisição ou dados não encontrados.')
            return {"status": "not_found"}, 404

    def print_label(self, data):
        melhorenvio_id = data.get('melhorenvio_id')
        if not melhorenvio_id:
            return {"error": "melhorenvio_id não informado"}, 400

        url = f"{self.baseUrl}/me/shipment/print"  # corrigi a URL

        payload = {"orders": [melhorenvio_id]}

        response = self.make_request(url, "post", payload)

        # aqui você pode tratar a resposta conforme o formato que make_request retorna
        return response

     
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
        melhorenvio_id = data['melhorenvio_id']
        
        url = f"{self.baseUrl}/me/cart/{melhorenvio_id}"
       
        item_data = self.make_request(url, "get")

        if item_data:
            print('Item encontrado no carrinho:', item_data)
            return {"status": "success", "data": item_data}, 200
        else:
            print('Erro na requisição ou dados não encontrados.')
            return {"status": "not_found"}, 404

    def pdfTag(self, data):
        melhorenvio_id = data.get('melhorenvio_id')
        if not melhorenvio_id:
            return {"error": "melhorenvio_id não fornecido"}, 400

        url = f"{self.baseUrl}/me/imprimir/zpl/pdf/{melhorenvio_id}"
        headers = self.headers.copy()
        headers["Accept"] = "application/json"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                try:
                    pdf_urls = response.json()
                except ValueError:
                    return {"error": "Erro ao parsear JSON"}, 500

                if not pdf_urls or not isinstance(pdf_urls, list):
                    return {"error": "Nenhuma URL de PDF encontrada"}, 404

                pdf_url = pdf_urls[0]
                pdf_response = requests.get(pdf_url)
                if pdf_response.status_code == 200:
                    if 'application/pdf' in pdf_response.headers.get('Content-Type', ''):
                        return Response(pdf_response.content, mimetype='application/pdf')
                    else:
                        return {"error": "Conteúdo não é PDF"}, 415
                else:
                    return {"error": "Falha ao baixar PDF"}, pdf_response.status_code
            else:
                return {"error": "Resposta não é JSON"}, 415
        else:
            return {"error": "Erro na requisição à API do Melhor Envio"}, response.status_code

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

