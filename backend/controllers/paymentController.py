from models.payment import Payment
from models.delivery import Delivery;
import os
from dotenv import load_dotenv
import requests
from models.payment import Payment
import uuid

load_dotenv()

class PaymentController:
    def processar_pagamento(dados_pagamento):
        try:
            payment = Payment(
                payment_id=dados_pagamento['payment_id'],
                total_value=dados_pagamento['total_value'],
                payment_date=dados_pagamento.get('date_approved'),
                payment_type=dados_pagamento['payment_type'],
                cpf=dados_pagamento.get('cpf'),
                email=dados_pagamento.get('email'),
                status=dados_pagamento.get('status', 'pendente'),
                usuario_id=dados_pagamento['usuario_id'],
                produtos=dados_pagamento['produtos']
            )
            payment.save()

            address_data = dados_pagamento.get('address')

            if address_data:
                delivery = Delivery(
                    usuario_id=dados_pagamento['usuario_id'],
                    user_name=address_data.get('user_name'),
                    recipient_name=address_data.get('recipient_name'),
                    street=address_data.get('street'),
                    number=address_data.get('number'),
                    complement=address_data.get('complement'),
                    city=address_data.get('city'),
                    state=address_data.get('state'),
                    zip_code=address_data.get('zip_code'),
                    country=address_data.get('country'),
                    bairro=address_data.get('bairro'),
                    phone=address_data.get('phone')
                )
               
                delivery.save()
            return {'message': 'Pagamento salvo com sucesso.'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
        
    def get_payment(payment_id):

        try:
            url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
            headers = {  
                "Authorization": f"Bearer {os.getenv('MERCADO_PAGO_ACCESS_TOKEN_TEST')}",
              
            }

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
                #payment_data = response.json()
                # payment = Payment(
                #     id=payment_data['id'],
                #     status=payment_data['status'],
                #     total_value=payment_data['transaction_amount'],
                #     payment_date=payment_data.get('date_approved'),
                #     payment_type=payment_data['payment_type'],
                #     email=payment_data.get('payer', {}).get('email'),
                #     cpf=payment_data.get('payer', {}).get('identification', {}).get('number'),
                #     usuario_id=payment_data.get('metadata', {}).get('usuario_id'),
                #     produtos=payment_data.get('metadata', {}).get('produtos')
                # )
                # return payment
            else:
                print(f"Erro ao buscar pagamento: {response.status_code} - {response.text}")
                return None
           
        except Exception as e:
            return {
                'status': 500,
                'message': 'Erro interno ao buscar pagamento.',
                'error': str(e)
            }, 500
        
    @staticmethod
    def update_status_payment(payment_id, status):
        try:
            if not payment_id or not status:
                return {"error": "payment_id e status são obrigatórios."}, 400

            updated = Payment.update_status(payment_id, status)

            if updated:
                return {"message": f"Status do pagamento {payment_id} atualizado para {status}."}, 200
            else:
                return {"error": f"Pagamento {payment_id} não encontrado."}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def get_payment_details(payment_id):
        payment = Payment.fetch_from_mercado_pago(payment_id)
        if payment:
            return {
                "id": payment.get("id"),
                "status": payment.get("status"),
                "amount": payment.get("transaction_amount"),
                "payer_email": payment.get("payer", {}).get("email"),
                "method": payment.get("payment_method_id"),
                "created": payment.get("date_created"),
            }
        return None
    
    @staticmethod
    def update_payment_data(payment_id, data):
        payload = {
            "status": data.get("status"),  
            "transaction_amount": data.get("amount"),
        }

        payment = Payment.fetch_from_mercado_pago(payment_id, payload)
       

        
        if isinstance(payment, dict) and "error" in payment:
            
            return {"error": payment["error"]}, 400

        
        if isinstance(payment, requests.Response):
            if payment.status_code == 200:
                return payment.json() 
            else:
                return {"error": payment.text}, payment.status_code
        else:
            return {"error": "Resposta inválida da API."}, 500


    @staticmethod
    def payment_chargeback(payment_id):
        payment = Payment.payment_chargeback_mercado_pago(payment_id)

        print(payment)
        # Verifique se o retorno da função é um dicionário de erro
        if isinstance(payment, dict) and "error" in payment:
            # Se for um erro, retorna a mensagem de erro
            return {"error": payment["error"]}, 400

        # Se for uma resposta de sucesso, verifica o status_code
        if isinstance(payment, requests.Response):
            if payment.status_code == 200:
                return payment.json()  # Retorna o pagamento atualizado
            else:
                return {"error": payment.text}, payment.status_code
        else:
            return {"error": "Resposta inválida da API."}, 500

    @staticmethod    
    def payment_refund(payment_id, data):
        payload = {
            "amount": data.get('amount')  # Certifique-se de passar o valor correto para o reembolso
        }
        payment = Payment.refund_payment_mercado_pago(payment_id, payload)
        print(payment)
        # Verifique se o retorno da função é um dicionário de erro
        if isinstance(payment, dict) and "error" in payment:
            # Se for um erro, retorna a mensagem de erro
            return {"error": payment["error"]}, 400
        # Se for uma resposta de sucesso, verifica o status_code