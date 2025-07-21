from flask import Flask, Blueprint, request, jsonify
from controllers.paymentController import PaymentController
import os



webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['GET', 'POST'])
def handle_webhook():
    if request.method == 'GET':
        return "Webhook endpoint is up", 200

    # Verificação opcional de assinatura
    expected_token = os.getenv("MP_WEBHOOK_SECRET")
    if expected_token and request.headers.get("x-mp-signature") != expected_token:
        print("Webhook rejeitado: token inválido")
        return jsonify({'status': 'unauthorized'}), 401

    data = request.get_json()
    print("📥 Webhook recebido:", data)

    if not data or data.get('type') != 'payment':
        return jsonify({'status': 'error', 'message': 'Invalid or unsupported webhook event'}), 400

    payment_id = data.get('data', {}).get('id')
    if not payment_id:
        return jsonify({'status': 'error', 'message': 'Missing payment ID'}), 400

    payment = PaymentController.get_payment(payment_id)
    print("🔍 Pagamento retornado:", payment)

    if not isinstance(payment, dict):
        return jsonify({'status': 'error', 'message': 'Invalid payment data returned'}), 400

    status = payment.get('status')
    external_reference = payment.get('external_reference')
    transaction_amount = payment.get('transaction_amount')

    print(f"✅ Payment ID: {payment_id} | Status: {status}")

    if status in ['approved', 'in_process', 'rejected']:
        response, status_code = PaymentController.update_status_payment(payment_id, status)
        print("🔄 Status atualizado:", response)
        return jsonify({
            'status': 'success',
            'message': f'Webhook processed for payment ID: {payment_id}',
            'payment_status': status,
            'external_reference': external_reference,
            'transaction_amount': transaction_amount
        }), 200

    return jsonify({'status': 'ignored', 'message': f'Status {status} não tratado'}), 200