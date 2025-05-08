from flask import Blueprint, request, jsonify
from datetime import datetime
from models.order import Order
orders_bp = Blueprint('order', __name__)

@orders_bp.route('/get-orders', methods=['GET'])
def get_orders():
    orders = Order.get_all()
    return jsonify([orders])

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