from models.payment import Payment

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
            return {'message': 'Pagamento salvo com sucesso.'}, 201
        except Exception as e:
            return {'error': str(e)}, 500