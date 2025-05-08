from models.payment import Payment
from models.delivery import Delivery;
import os
from dotenv import load_dotenv

load_dotenv()

class PaymentController:
    def processar_pagamento(dados_pagamento):
        try:
            payment = Payment(
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
                print('Delivery', delivery)
                delivery.create()
            return {'message': 'Pagamento salvo com sucesso.'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
        
    def get_payment(payment_id):
        try:
            url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
            headers = {  
                "Authorization": f"Bearer {os.getenv('MERCADOPAGO_ACCESS_TOKEN')}"
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
            payment = Payment.get_payment_by_id(payment_id)
            if payment:
                return {
                    'status': 200,
                    'message': 'Pagamento encontrado com sucesso.',
                    'payment': payment
                }, 200
            else:
                return {
                    'status': 404,
                    'message': 'Pagamento não encontrado.'
                }, 404
        except Exception as e:
            return {
                'status': 500,
                'message': 'Erro interno ao buscar pagamento.',
                'error': str(e)
            }, 500