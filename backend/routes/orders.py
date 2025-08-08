from flask import Blueprint, request, jsonify, send_file, abort
from datetime import datetime
from models.order import Order

orders_bp = Blueprint('order', __name__)

@orders_bp.route('/get-orders', methods=['GET'])
def get_orders():
    orders = Order.get_all()
    return jsonify([orders])

@orders_bp.route('/get-order/<user_id>', methods=['GET'])
def get_order_by_userId(user_id):
    user_id = user_id.lstrip('/')
    order = Order.get_by_user_id(user_id)
    if order:
        return jsonify(order)
    else:
        return jsonify({'message': 'Pedido não encontrado'}), 404

@orders_bp.route('/create-orders', methods=['POST'])
def create_order():
    data = request.get_json()

    try:
        # Extrair os dados da requisição
        user_id = data['user_id']
        payment_id = data.get('payment_id')  # opcional
        shipment_info = data.get('shipment_info', '')
        total_amount = data['total_amount']
        items = data['items']  # lista de dicionários com "product_id", "quantity" e "unit_price"

        # Criar uma instância do pedido
        order = Order(user_id, payment_id, shipment_info, total_amount, items)
        
        # Salvar o pedido no banco de dados
        order_id = order.save()

        return jsonify({'message': 'Pedido criado com sucesso!', 'order_id': order_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@orders_bp.route('/<int:order_id>/download', methods=['GET'])
def pdf_download(order_id):
    order = Order.query.get(order_id)
    if not order:
        abort(404, description="Pedido não encontrado")

    buffer = order.generate_pdf()

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"Pedido_{order_id}.pdf",
        mimetype='application/pdf'
    )
