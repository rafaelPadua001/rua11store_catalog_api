import mercadopago
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from models.payment import Payment
import uuid
import requests
import re
from datetime import datetime

load_dotenv()

def get_mercado_sdk():
        access_token = os.getenv("MERCADO_PAGO_ACCESS_TOKEN_TEST")
       # print("Access Token:", os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST'))

        if not access_token:
            raise RuntimeError("Variavel Access token nao definida")
        return mercadopago.SDK(access_token)

sdk = get_mercado_sdk()


class PaymentStrategy(ABC):
    
    @abstractmethod
    def create_payment(self, data):
        pass

class CreditCardPayment(PaymentStrategy):
    def create_payment(self, data):
        coupon_amount = float(data.get("coupon_amount", 0))
        coupon_code = data.get("coupon_code")

        url = "https://api.mercadopago.com/v1/payments"
        headers = {
            "X-Idempotency-Key": str(uuid.uuid4()),
            "Authorization": f"Bearer {os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')}",
            "Content-Type": "application/json"
        }

        payment_data = {
            "transaction_amount": float(data["total"]),
            "token": data["card_token"],
            "description": data.get("description", "Compra com cartão de crédito"),
            "installments": int(data["installments"]),
            "payment_method_id": data.get("payment_method_id", "visa"),
            "capture": True,
            "external_reference": f"pedido_{uuid.uuid4()}",
            "payer": {
                "email": data["payer_email"],
                "identification": {
                    "type": "CPF",
                    "number": data["payer_cpf"]
                },
                "entity_type": "individual",
                "type": "customer"
            },
            "metadata": {
                "coupon_code": coupon_code,
                "coupon_amount": coupon_amount,
            },
            "additional_info": {
                "items": [
                    {
                        "id": item.get("id", "SKU123"),
                        "title": item.get("title", "Produto"),
                        "description": item.get("description", "Produto comprado"),
                        "category_id": item.get("category", "services"),
                        "quantity": item.get("quantity", 1),
                        "unit_price": float(item.get("unit_price", data["total"]))  # fallback para valor total
                    }
                    for item in data.get("products", [])
                ],
                "payer": {
                    "first_name": data.get("payer_first_name", "Test"),
                    "last_name": data.get("payer_last_name", "User"),
                    "phone": {
                        "area_code": data.get("area_code", "11"),
                        "number": data.get("phone_number", "999999999")
                    },
                    "address": {
                        "zip_code": data.get("zip_code", "00000-000"),
                        "street_name": data.get("street_name", "Rua Exemplo"),
                        "street_number": data.get("street_number", 123)
                    }
                }
            }
            
        }

        response = requests.post(url, headers=headers, json=payment_data)
        result = response.json()

        if response.status_code == 201:
            payment = Payment(
                payment_id=result.get("id"),
                total_value=result.get("transaction_amount"),
                payment_date=result.get("date_approved"),
                payment_type="crédito",
                cpf=data["payer_cpf"].replace(".", "").replace("-", "").strip(),
                email=data["payer_email"],
                status=result["status"],
                usuario_id=data["userId"],
                products=data["products"],
                address=data.get("address"),
                coupon_code=coupon_code,
                coupon_amount=coupon_amount
            )
            payment.save()

            if result.get("status") == "rejected":
                return {
                    "status": 400,
                    "message": "Pagamento não aprovado. Verifique os dados do cartão ou use outro método.",
                    "error": result.get("status_detail")
                }

            return result

        return {
            "status": response.status_code,
            "message": "Erro ao criar pagamento.",
            "error": result
        }


    
class DebitCardPayment(PaymentStrategy):
   def create_payment(self, data):
    cpf_limpo = re.sub(r'\D', '', data["payer_cpf"])
    coupon_amount = float(data.get("coupon_amount", 0))
    coupon_code = data.get("coupon_code")

    url = "https://api.mercadopago.com/v1/payments"
    headers = {
        "X-Idempotency-Key": str(uuid.uuid4()),
        "Authorization": f"Bearer {os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')}",  # use TEST token
        "Content-Type": "application/json"
    }

    payment_data = {
        "transaction_amount": float(data["total"]),
        "token": data["card_token"],
        "description": data.get("description", "Compra com cartão de crédito"),
        "installments": int(data["installments"]),  # 1 se for débito simulado
        "payment_type_id": "debit_card",
        "payment_method_id": data.get("payment_method_id", "visa"),  # "visa", "master", etc
        "payer": {
            "email": data["payer_email"],
            "identification": {
                "type": "CPF",
                "number": cpf_limpo
            },
            "entity_type": "individual",
            "type": "customer"
        },
        "metadata": {
            "coupon_code": coupon_code,
            "coupon_amount": coupon_amount,
        },
        
    }

    print("➡️ Enviando dados para pagamento Mercado Pago:")
    print(payment_data)

    response = requests.post(url, headers=headers, json=payment_data)
    
    result = response.json()
    print("❗️Resposta do Mercado Pago:")
    print(result)
    print(response)
    if response.status_code == 201:
        # pagamento aprovado
        payment = Payment(
            payment_id=result.get("id"),
            total_value=result.get("transaction_amount"),
            payment_date=result.get("date_approved"),
            payment_type="débito",  # trocado para refletir o teste
            cpf=cpf_limpo,
            email=data["payer_email"],
            status=result["status"],
            usuario_id=data["userId"],
            products=data["products"],
            address=data.get("address"),
            coupon_code=coupon_code,
            coupon_amount=coupon_amount
        )
        payment.save()

        if result.get("status") == "rejected":
            return {
                "status": 400,
                "message": "Pagamento não aprovado. Verifique os dados do cartão ou use outro método.",
                "error": result.get("status_detail")
            }

        return result

    # Falha
    return {
        "status": response.status_code,
        "message": "Erro ao criar pagamento.",
        "error": result
    }

class PixPayment(PaymentStrategy):
    def create_payment(self, data):
        coupon_amount = float(data.get("coupon_amount", 0))
        coupon_code = data.get("coupon_code")
        payment_data = {
            "transaction_amount": float(data["total"]),
            "description": data.get("description", "Pagamento via Pix"),
            "payment_method_id": "pix",
            "payer": {
                "email": data["payer_email"],
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
            },
            "metadata": {
                "coupon_code": coupon_code,
                "coupon_amount": coupon_amount,
            },
        }

        response = sdk.payment().create(payment_data)['response']

        pix_info = {
            "id": response.get("id"),
            "status": response.get("status"),
            "status_detail": response.get("status_detail"),
            "qr_code": response.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code"),
            "qr_code_base64": response.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code_base64")
        }

        # Aqui: criar um objeto do seu model de pagamento
        payment = Payment(
            payment_id=pix_info["id"],
            status=pix_info["status"],
          #  status_detail=pix_info["status_detail"],
            #qr_code=pix_info["qr_code"],
            #qr_code_base64=pix_info["qr_code_base64"],
            total_value=payment_data["transaction_amount"],
            #payer_email=data["payer_email"],
            #description=payment_data["description"],
            payment_date=datetime.now(),
            payment_type="pix",
            cpf=data["payer_cpf"],
            email=data["payer_email"],
            usuario_id=data["userId"],
            products=data["products"],
            address=data.get("address"),
            coupon_code=coupon_code,
            coupon_amount=coupon_amount
        )

        # Salva no banco
        payment.save()

        return pix_info
