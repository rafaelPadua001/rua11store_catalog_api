from flask import Blueprint, request, jsonify
from models.PaymentProcessor import PaymentProcessor
from services.mercadoPago_service import (
    CreditCardPayment,
    DebitCardPayment,
    PixPayment
)

mercadoPago_bp = Blueprint("payment", __name__)



@mercadoPago_bp.route("/payment", methods=["POST"])
def payment():
    data = request.json
    payment_type = data.get('paymentType')
    
    print(data)
    processor = None

    if payment_type == "credit":
        processor = PaymentProcessor(CreditCardPayment())
    elif payment_type == "debit":
        processor = PaymentProcessor(DebitCardPayment())
    elif payment_type == "pix":
        processor = PaymentProcessor(PixPayment())
    else:
        return jsonify({"error": "Método de pagamento inválido"}), 400
    
    result = processor.process_payment(data)
    return jsonify(result)
