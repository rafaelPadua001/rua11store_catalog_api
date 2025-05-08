import os
import requests
from dotenv import load_dotenv

load_dotenv()  # auto load .env

class MelhorEnvioService:
    def __init__(self):
        self.baseUrl = "https://sandbox.melhorenvio.com.br/api/v2"
        self.token = os.getenv("MELHOR_ENVIO_TOKEN")
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
            print(payload)
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print('Erro ao calcular frete:', e)
            if e.response is not None:
                print("Resposta da API:", e.response.text)
            return None

    def _generate_package(self, products):
        if not products:
            return {}
        
        produto = products[0]
        return {
            "height": produto["height"],
            "width": produto["width"],
            "length": produto["length"],
            "weight": produto["weight"]
        }
