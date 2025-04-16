from flask import Blueprint, jsonify
from models.payment import Payment

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