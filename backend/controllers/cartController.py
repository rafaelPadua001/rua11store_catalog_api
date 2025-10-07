from models.cart import Cart
from models.cartItems import CartItems
from database import db
from controllers.cartItemController import CartItemController
from flask import jsonify

class CartController:
    def get_cart_items(user_id):
        results = (
            db.session.query(Cart, CartItems)
            .outerjoin(CartItems, Cart.id == CartItems.cart_id)
            .filter(Cart.user_id == user_id)
            .all()
        )

        if not results:
            return jsonify({"message": "nenhum carrinho encontrado."}), 404

        carts_dict = {}

        for cart, item in results:
            if cart.id not in carts_dict:
                carts_dict[cart.id] = {
                    "id": cart.id,
                    "user_id": cart.user_id,
                    "created_at": cart.created_at,
                    "items": []
                }
            if item:
               carts_dict[cart.id]["items"].append({
                    "id": item.id,
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "product_price": item.product_price,
                    "product_image": item.product_image,
                    "quantity": item.quantity,
                    "product_height": item.product_height,
                    "product_width": item.product_width,
                    "product_weight": item.product_weight,
                    "product_length": item.product_length
                })



        return jsonify(list(carts_dict.values())), 200

    

    def add_cart(user_id, product, quantity=1):
        #search user cart or create a new
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()

        # call cart item controller
        cart_item = CartItemController.add_cart_item(
            cart_id = cart.id,
            user_id = user_id,
            product = product,
            quantity = quantity

        )

        item_data = {
            "id": cart_item.id,
            "cart_id": cart_item.cart_id,
            "product_id": cart_item.product_id,
            "user_id": cart_item.user_id,
            "product_name": cart_item.product_name,
            "product_price": str(cart_item.product_price),
            "product_height": cart_item.product_height,
            "product_width": cart_item.product_width,
            "product_weight": cart_item.product_weight,
            "product_length": cart_item.product_length,
            "quantity": cart_item.quantity,
            "created_at": cart_item.created_at.isoformat()
        }

        return jsonify({'msg': 'Item adicionado ao carrinhjo', "items": item_data})
    
    

