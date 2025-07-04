from flask import Flask, Blueprint, request, jsonify
from controllers.paymentController import PaymentController


webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['GET','POST'])
def handle_webhook():
    if request.method == 'GET':
        return "Webhook endpoint is up", 200
    data = request.get_json()
    print("Received webhook data:", data)

    if data and 'type' in data and data['type'] == 'payment':
        payment_id = data.get('data', {}).get('id')
        payment = PaymentController.get_payment(payment_id)
        print(type(payment))
        if payment:
            status = payment.get('status') 
            external_reference = payment.get('external_reference')
            transaction_amount = payment.get('transaction_amount')

            print(f"Payment ID: {payment_id}")
            print(f"Status: {status}")  

            if status in ['approved', 'in_process', 'rejected']:
                print(f"Payment {payment_id} has status {status}.")
                response, status_code = PaymentController.update_status_payment(payment_id, status)
                print(response)

             #   pass

            return jsonify({
                'status': 'success',
                'message': f'Webhook processed for payment ID: {payment_id}',
                'status': status,
                'external_reference': external_reference,
                'transaction_amount': transaction_amount
            }), 200

        
    return jsonify({
        'status': 'error',
        'message': 'Invalid webhook data'
    }), 400