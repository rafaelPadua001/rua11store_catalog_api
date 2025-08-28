from flask import Flask, Blueprint, request, jsonify
from controllers.paymentController import PaymentController
import os
from models.delivery import Delivery
from database import db
from models import Delivery, Order, Payment
from controllers.emailController import EmailController


webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['GET', 'POST'])
def handle_webhook():
    if request.method == 'GET':
        return "Webhook endpoint is up", 200

    # Verificação opcional de assinatura
    expected_token = os.getenv("MP_WEBHOOK_SECRET")
    #if expected_token and request.headers.get("x-mp-signature") != expected_token:
    #    print("Webhook rejeitado: token inválido")
    #    return jsonify({'status': 'unauthorized'}), 401

    data = request.get_json()
    print("📥 Webhook recebido:", data)

    if not data or data.get('type') != 'payment':
        return jsonify({'status': 'error', 'message': 'Invalid or unsupported webhook event'}), 400

    payment_data = data.get('data', {})
    payment_id = payment_data.get('id')
    if not payment_id:
        return jsonify({'status': 'error', 'message': 'Missing payment ID'}), 400

    payment = PaymentController.get_payment(payment_id)
    print("🔍 Pagamento retornado:", payment)

    if not isinstance(payment, dict):
        return jsonify({'status': 'error', 'message': 'Invalid payment data returned'}), 400

    status = payment.get('status', 'pending')
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


@webhook_bp.route('/melhor-envio/webhook', methods=['POST'])
def handle_melhorEnvio_webhook():
    data = request.get_json(force=True, silent=True) or {}
    
    #print("📦 Payload recebido:", data)   
    event = data.get('event')
   
    if event == 'webhook.ping':
        jsonify({"message": "Webhook verificado com sucesso"}), 200

    resource = data.get('resource') or data.get('data')
    shipment_id = resource.get('id') if resource else None

    if not shipment_id:
        return jsonify({"message": "Webhook verificado com sucesso"}), 200

    delivery = Delivery.query.filter_by(melhorenvio_id=shipment_id).first()
    if not delivery:
        return jsonify({"error": "Delivery não encontrado"}), 404

    # Map event to intern status
    event_status_map = {
        "shipment.created": "created",
        "shipment.updated": "updated",
        "shipment.deleted": "deleted",
        "shipment.canceled": "canceled",
        "shipment.printed": "printed",
        "shipment.purchased": "purchased",
    }

    # update status delivery
    if event in event_status_map:
        delivery.status = event_status_map[event]
        db.session.commit()

        #found payer email
        payment_email = (
            db.session.query(Payment.email)
            .join(Order, Payment.id == Order.payment_id)
            .filter(Order.delivery_id == delivery.id)
            .first()
        )

        if payment_email and payment_email[0]:
            try:
                body_text = f"O status da sua entrega foi atualizado para: {delivery.status}"
                html_message = f'<p style="text-align: center;">{body_text}</p>'

                if event == "shipment.purchased":
                    tracking_code = resource.get('tracking_code') or resource.get('tracking') or resource.get('tracking_number') or ""
                    if tracking_code:
                        rastreio_url = f"https://www.melhorrastreio.com.br/rastreamento/{tracking_code}"

                        button_html = f'<div style="text-align:center; margin-top:20px;">' \
                                        f'<a href="{rastreio_url}" style="background-color:#28a745; color:#fff; padding:12px 24px; text-decoration:none; border-radius:5px; font-weight:bold; display:inline-block;">Rastreie seu pedido</a>' \
                                        '</div>'


                        html_message += button_html

                EmailController.send_email(
                    recipients=[payment_email[0]],
                    subject="Atualização no status da sua entrega",
                    body=body_text,
                    html = html_message
                )
            except Exception as e:
                print(f"❌ Erro ao enviar email: {e}")

        return jsonify({"message": f"Delivery status updated to '{delivery.status}'"}), 200
      
    return jsonify({"message": f"Event '{event}' ignorado"}), 200