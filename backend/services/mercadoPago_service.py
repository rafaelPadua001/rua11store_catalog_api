import mercadopago
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from models.payment import Payment
import uuid
from uuid import uuid4
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
        payer_email = data.get("payer_email") or data.get('email')
        payer_cpf = data.get("payer_cpf") or data.get('cpf')
        payer_name = data.get("payer_name") or data.get('name')

        card_token = self.create_card_token(data)
        if not card_token:
            return {
                "status": 400,
                "message": "Falha ao criar token do cartão"
            }

        url = "https://api.mercadopago.com/v1/payments"
        headers = {
            "X-Idempotency-Key": str(uuid.uuid4()),
            "Authorization": f"Bearer {os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')}",
            "Content-Type": "application/json"
        }

        payment_data = {
            "transaction_amount": float(data["total"]),
            "token": card_token,
            "description": data.get("description", "Compra com cartão de crédito"),
            "installments": int(data["installments"]),
            "payment_method_id": data.get("payment_method_id", "visa"),
            "capture": True,
            "external_reference": f"pedido_{uuid.uuid4()}",
            "payer": {
                "email": payer_email,
                "identification": {
                    "type": "CPF",
                    "number": payer_cpf
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
                    "first_name":  payer_name.split(' ')[0] if payer_name else "Test",
                    "last_name": " ".join(payer_name.split(' ')[1:]) if payer_name else "User",
                    "phone": {
                        "area_code": data.get("area_code", "11"),
                        "number": data.get("phone_number", "999999999")
                    },
                    "address": {
                        "zip_code": data.get("zip_code", "00000-000"),
                        "street_name": data.get("street_name", "Rua Exemplo"),
                        "street_number": data.get("street_number", 123),
                       
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
                cpf=payer_cpf.replace(".", "").replace("-", "").strip(),
                email=payer_email,
                name=payer_name,
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
    
    def create_card_token(self, data):
        """Cria o token do cartão usando a API do Mercado Pago"""
        try:
            # ⚡ Extrai dados do cartão do payload
            card_data = data.get("card_data", {})
          
            
            token_url = "https://api.mercadopago.com/v1/card_tokens"
            headers = {
                "Authorization": f"Bearer {os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')}",
                "Content-Type": "application/json"
            }

            token_payload = {
                "card_number": card_data.get("card_number", "").replace(" ", ""),
                "expiration_month": int(card_data.get("expiration_month", 0)),
                "expiration_year": int(card_data.get("expiration_year", 0)),
                "security_code": card_data.get("security_code", ""),
                "cardholder": {
                    "name": data.get("name", ""),
                    "identification": {
                        "type": "CPF",
                        "number": data["cpf"].replace(".", "").replace("-", "").strip()
                    }
                }
            }

            print("🔄 Criando token do cartão:", token_payload)

            response = requests.post(token_url, headers=headers, json=token_payload)
            result = response.json()

            if response.status_code == 201:
                print("✅ Token criado com sucesso:", result.get("id"))
                return result.get("id")
            else:
                print("❌ Erro ao criar token:", result)
                return None

        except Exception as e:
            print("❌ Exception ao criar token:", str(e))
            return None


    
class DebitCardPayment(PaymentStrategy):
    def create_payment(self, data):
        try:
            coupon_amount = float(data.get("coupon_amount", 0))
            coupon_code = data.get("coupon_code")
            
            # ⚡ CORREÇÃO: Usar campos com fallback
            payer_email = data.get("payer_email") or data.get('email')
            payer_cpf = data.get("payer_cpf") or data.get('cpf')
            cpf_limpo = re.sub(r'\D', '', payer_cpf)
            payer_name = data.get("payer_name") or data.get('name')

            # ⚡ CORREÇÃO: Criar token do cartão primeiro (igual ao crédito)
            card_token = self._create_card_token(data)
            if not card_token:
                return {
                    "status": 400,
                    "message": "Falha ao criar token do cartão"
                }

            url = "https://api.mercadopago.com/v1/payments"
            headers = {
                "X-Idempotency-Key": str(uuid.uuid4()),
                "Authorization": f"Bearer {os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')}",
                "Content-Type": "application/json"
            }

            payment_data = {
                "transaction_amount": float(data["total"]),
                "token": card_token,  # ⚡ CORREÇÃO: Usar token criado
                "description": data.get("description", "Compra com cartão de débito"),
                "installments": 1,
                "payment_method_id": data.get("payment_method_id", "debit_card"),
                "capture": True,  # ⚡ Adicionar capture
                "external_reference": f"pedido_{uuid.uuid4()}",  # ⚡ Adicionar reference
                "payer": {
                    "email": payer_email,
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
                "additional_info": {  # ⚡ Adicionar additional_info
                    "items": [
                        {
                            "id": item.get("id", "SKU123"),
                            "title": item.get("title", "Produto"),
                            "description": item.get("description", "Produto comprado"),
                            "category_id": item.get("category", "services"),
                            "quantity": item.get("quantity", 1),
                            "unit_price": float(item.get("unit_price", data["total"]))
                        }
                        for item in data.get("products", [])
                    ],
                    "payer": {
                        "first_name": payer_name.split(' ')[0] if payer_name else "Test",
                        "last_name": " ".join(payer_name.split(' ')[1:]) if payer_name else "User",
                        "phone": {
                            "area_code": data.get("area_code", "11"),
                            "number": data.get("phone_number", "999999999")
                        },
                        "address": {
                            "zip_code": data.get("zip_code", "00000-000"),
                            "street_name": data.get("street_name", "Rua Exemplo"),
                            "street_number": data.get("street_number", 123),
                        }
                    }
                }
            }

            print("➡️ Enviando dados para pagamento débito Mercado Pago:")
            print(payment_data)

            response = requests.post(url, headers=headers, json=payment_data)
            result = response.json()
            
            print(f"❗️Resposta do Mercado Pago (Débito): Status {response.status_code}")
            print(result)

            if response.status_code == 201:
                # ⚡ CORREÇÃO: Usar campos com fallback ao salvar
                payment = Payment(
                    payment_id=result.get("id"),
                    total_value=result.get("transaction_amount"),
                    payment_date=result.get("date_approved"),
                    payment_type="débito",
                    cpf=cpf_limpo,
                    email=payer_email,  # ⚡ CORREÇÃO: usar payer_email
                    name=payer_name,    # ⚡ CORREÇÃO: adicionar name
                    status=result["status"],
                    usuario_id=data.get("userId"),
                    products=data.get("products", []),
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

                return {
                    "status": 201,
                    "payment_id": result.get("id"),
                    "status": result.get("status"),
                    "message": "Pagamento com débito processado com sucesso"
                }

            # Falha
            return {
                "status": response.status_code,
                "message": "Erro ao criar pagamento com débito.",
                "error": result
            }

        except Exception as e:
            print(f"❌ Erro no processamento de débito: {str(e)}")
            import traceback
            print(f"❌ Traceback: {traceback.format_exc()}")
            return {
                "status": 500,
                "message": "Erro interno no processamento do pagamento com débito",
                "error": str(e)
            }

    def _create_card_token(self, data):
        """Cria o token do cartão - mesma lógica do crédito"""
        try:
            card_data = data.get("card_data", {})
            
            # ⚡ CORREÇÃO: Garantir que o ano tenha 4 dígitos
            expiration_year = card_data.get("expiration_year", "")
            if expiration_year and len(expiration_year) == 2:
                expiration_year = f"20{expiration_year}"
                print(f"🔧 Ano corrigido (débito): {expiration_year}")
            
            token_url = "https://api.mercadopago.com/v1/card_tokens"
            headers = {
                "Authorization": f"Bearer {os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')}",
                "Content-Type": "application/json"
            }

            payer_email = data.get("payer_email") or data.get('email')
            payer_cpf = data.get("payer_cpf") or data.get('cpf')
            payer_name = data.get("payer_name") or data.get('name')

            token_payload = {
                "card_number": card_data.get("card_number", "").replace(" ", ""),
                "expiration_month": int(card_data.get("expiration_month", 0)),
                "expiration_year": int(expiration_year),
                "security_code": card_data.get("security_code", ""),
                "cardholder": {
                    "name": payer_name,
                    "identification": {
                        "type": "CPF",
                        "number": payer_cpf.replace(".", "").replace("-", "").strip()
                    }
                }
            }

            print("🔄 Criando token para débito:", {**token_payload, "security_code": "***"})

            response = requests.post(token_url, headers=headers, json=token_payload)
            result = response.json()

            print(f"📨 Resposta token débito: Status {response.status_code}")

            if response.status_code == 201:
                print("✅ Token débito criado:", result.get("id"))
                return result.get("id")
            else:
                print("❌ Erro ao criar token débito:", result)
                return None

        except Exception as e:
            print("❌ Exception ao criar token débito:", str(e))
            return None

class PixPayment(PaymentStrategy):
    def create_payment(self, data):
        # Valores do cupom
        coupon_amount = float(data.get("coupon_amount", 0))
        coupon_code = data.get("coupon_code")

        # Separar nome e sobrenome
        full_name = data.get("payer_name", "")
        first_name, last_name = (full_name.split(" ")[0], " ".join(full_name.split(" ")[1:])) if full_name else ("Cliente", "")

        # Monta dados do pagamento
        payment_data = {
            "transaction_amount": float(data["total"]),
            "description": data.get("description", "Pagamento via Pix"),
            "payment_method_id": "pix",
            "payer": {
                "email": data["payer_email"],
                "first_name": first_name,
                "last_name": last_name,
                "identification": {
                    "type": "CPF",
                    "number": data["payer_cpf"]
                },
               # "address": data.get("address", {
               #     "zip_code": "00000000",
               #     "street_name": "Desconhecido",
               #     "street_number": "0",
               #     "neighborhood": "Desconhecido",
               #     "city": "Desconhecido",
               #     "federal_unit": "XX"
               # })
            },
            "metadata": {
                "coupon_code": coupon_code,
                "coupon_amount": coupon_amount,
            },
        }

        # Chama API do Mercado Pago
        response = sdk.payment().create(payment_data)['response']

        # Pega dados do Pix
        transaction_data = response.get("point_of_interaction", {}).get("transaction_data", {})
        qr_code = transaction_data.get("qr_code")
        qr_code_base64 = transaction_data.get("qr_code_base64")

        # Se a API não gerar ID, cria UUID temporário
        payment_id = response.get("id") or str(uuid4())

        pix_info = {
            "id": payment_id,
            "status": response.get("status", "pending"),
            "status_detail": response.get("status_detail"),
            "qr_code": qr_code,
            "qr_code_base64": qr_code_base64
        }

        # Cria Payment real
        payment = Payment(
            payment_id=payment_id,
            status=pix_info["status"],
            total_value=payment_data["transaction_amount"],
            payment_date=datetime.now(),
            payment_type="pix",
            cpf=data["payer_cpf"],
            email=data["payer_email"],
            name=data["payer_name"],
            usuario_id=data["userId"],
            products=data["products"],
            address=data.get("address"),
            coupon_code=coupon_code,
            coupon_amount=coupon_amount
        )

        # Salva no banco
        payment.save()

        return pix_info
