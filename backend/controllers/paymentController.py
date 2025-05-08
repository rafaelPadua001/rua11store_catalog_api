from models.payment import Payment
from models.delivery import Delivery;

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