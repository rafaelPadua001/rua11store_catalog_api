from flask import Blueprint, jsonify, request
from models.payment import Payment
from controllers.paymentController import PaymentController

payment_bp = Blueprint('payment_routes', __name__)

@payment_bp.route('/get-all', methods=["GET"])
def list_payments():
    try:
        payments = Payment.get_all_payments()
        return jsonify({
            "status": 200,
            "message": "Pagamentos encontrados com sucesso.",
            "payments": payments
        }), 200
    except Exception as e:
        print(f"Erro ao listar pagamentos: {e}")
        return jsonify({
            "status": 500,
            "message": "Erro interno ao buscar pagamentos.",
            "error": str(e)
        }), 500


@payment_bp.route("/payment/<payment_id>", methods=["GET"])
def get_payment(payment_id):
    payment_data = PaymentController.get_payment_details(payment_id)
    print(payment_data)
    if payment_data:
        return jsonify(payment_data)
    else:
        return jsonify({"error": "Pagamento não encontrado"}), 404
    
@payment_bp.route("/payment/update-status/<int:payment_id>", methods=["PUT"])
def update_payment_status(payment_id):
    # Extraímos os dados da requisição JSON
    data = request.get_json()

    if not data:
        return jsonify({"error": "Dados não fornecidos."}), 400
    
    # Printando os dados para verificar
    print(data)

    # Obtendo os detalhes do pagamento
    payment_data = PaymentController.get_payment_details(payment_id)
    if not payment_data:
        return jsonify({"error": "Pagamento não encontrado no Mercado Pago"}), 404

    try:
        # Atualizando os dados do pagamento
        updated = PaymentController.update_payment_data(payment_id, data)
        
        return jsonify({
            "message": "Pagamento atualizado com sucesso",
            "payment": updated
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@staticmethod    
@payment_bp.route("/payment/chargeback/<int:payment_id>", methods=["POST"])
def chargeback_payment(payment_id):
    payment_data = PaymentController.payment_chargeback(payment_id)
   
    if payment_data:
        return jsonify(payment_data)
    else:
        return jsonify({"error": "Pagamento não encontrado"}), 404

@staticmethod
@payment_bp.route("/payment/refund/<int:payment_id>", methods=["POST"])
def refund_payment(payment_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Dados não fornecidos."}), 400
    
   
    payment_data = PaymentController.payment_refund(payment_id, data)
   
    if payment_data:
        return jsonify(payment_data)
    else:
        return jsonify({"error": "Pagamento não encontrado"}), 404