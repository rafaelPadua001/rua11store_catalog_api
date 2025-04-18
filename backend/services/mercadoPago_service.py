import mercadopago
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from models.payment import Payment

load_dotenv()

def get_mercado_sdk():
        access_token = os.getenv("MERCADO_PAGO_ACCESS_TOKEN_TEST")
        if not access_token:
            raise RuntimeError("Variavel ACCess token nao definida")
        return mercadopago.SDK(access_token)

sdk = get_mercado_sdk()


class PaymentStrategy(ABC):
    
    @abstractmethod
    def create_payment(self, data):
        pass

class CreditCardPayment(PaymentStrategy):
    def create_payment(self, data):
       
        payment_data = {
           "transaction_amount": float(data["total"]),
            "token": data["card_token"],
            "description": data.get("description", "Compra com cartão de crédito"),
            "installments": int(data["installments"]),
            "payment_method_id": "visa",  # ou "master", "amex", etc.
            "payer": {
            "email": data["payer_email"],  # Certifique-se de que o e-mail está vindo corretamente
           # "first_name": data.get("first_name", "Nome"),  # Nome do pagador
           # "last_name": data.get("last_name", "Sobrenome"),  # Sobrenome do pagador
            "identification": {
                "type": "CPF",  # Pode ser "CPF" ou "CNPJ", dependendo do tipo de documento
                "number": data["payer_cpf"]  # CPF do pagador (certifique-se de ter essa informação)
            }
        }
        }
        response = sdk.payment().create(payment_data)
        print(response)

        result = response['response']

        if result.get("status") == "approved":
            payment = Payment(
                total_value=result.get("transaction_amount"),
                payment_date=result.get("date_approved"),  # vem em ISO8601
                payment_type="crédito",  # pois estamos usando cartão
                cpf=data["payer_cpf"],
                email=data["payer_email"],
                status=result["status"],
                usuario_id=data["userId"],
                products=data["products"]
            )

            payment.save()
        return response['response']
    
class DebitCardPayment(PaymentStrategy):
    def create_payment(self, data):
        payment_data = { 
            "transaction_amount": float(data["amount"]),
            "token": data["card_token"],
            "description": data.get("description", "Compra com cartão de débito"),
            "payment_method_id": data["payment_method_id"],
            "payer": {
                "email": data["payer_email"]
            }
        }
        return sdk.payment().crete(payment_data)['response']

class PixPayment(PaymentStrategy):
    def create_payment(self, data):
        payment_data = {
            "transaction_amount": float(data["amount"]),
            "description": data.get("description", "Pagamento via Pix"),
            "payment_method_id": "pix",
            "payer": {
                "email": data["payer_email"],
                "first_name": data["payer_first_name"],
                "last_name": data["payer_last_name"],
                "identification": {
                    "type": "CPF",
                    "number": data["payer_cpf"]
                },
                "address": {
                    "zip_code": "06233200",
                    "street_name": "Av. das Nações Unidas",
                    "street_number": "3003",
                    "neighborhood": "Bonfim",
                    "city": "Osasco",
                    "federal_unit": "SP"
                }
            }
        }
        return sdk.payment().create(payment_data)['response']