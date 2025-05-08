from flask import Flask, Blueprint, request, jsonify

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print("Received webhook data:", data)

    if data and 'type' in data and data['type'] == 'payment':
        payment_id = data.get('data', {}).get('id')

        return jsonify({
            'status': 'success',
            'message': f'Webhook received for payment ID: {payment_id}'
        }), 200
    
    return jsonify({
        'status': 'error',
        'message': 'Invalid webhook data'
    }), 400