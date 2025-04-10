import mercadopago
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

def get_mercado_sdk():
        sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_ACCESS_TOKEN_TEST"))
        if not sdk:
            raise RuntimeError("Variavel ACCess token nao definida")
        return mercadopago.SDK(sdk)


class PaymentStrategy(ABC):
    
    @abstractmethod
    def create_payment(self, data):
        pass

class CreditCardPayment(PaymentStrategy):
    def create_payment(self, data):
        payment_data = {
           "transaction_amount": float(data["amount"]),
            "token": data["card_token"],
            "description": data.get("description", "Compra com cartão de crédito"),
            "installments": int(data["installments"]),
            "payment_method_id": "visa",  # ou "master", "amex", etc.
            "payer": {
                "email": data["payer_email"]
            }
        }

        return sdk.payment().create(payment_data)['response']
    
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