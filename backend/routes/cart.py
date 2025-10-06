from flask import Blueprint, request, jsonify
from controllers.cartController import CartController
from controllers.cartItemController import CartItemController
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.product import Product
#from flask_cors import CORS

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

@cart_bp.route('/get-cart/<userId>', methods=["GET"])
@jwt_required()
def get_cart(userId):
    user_id = get_jwt_identity()
   
    return CartController.get_cart_items(user_id)

@cart_bp.route("/add-cart", methods=["POST"])
@jwt_required()
def add_cart():
    user_id = get_jwt_identity()  # pega o ID do usuário do token
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    # aqui você pode buscar o produto no DB
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"msg": "Produto não encontrado"}), 404

    return CartController.add_cart(user_id, product, quantity)

@cart_bp.route("/cart-item-remove/<int:itemId>", methods=["DELETE"])
@jwt_required()
def remove_item_cart(itemId):
    return CartItemController.remove_item_cart(itemId)