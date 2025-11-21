from models.cart import Cart
from models.cartItems import CartItems
from database import db
from controllers.cartItemController import CartItemController
from flask import jsonify
import uuid

class CartController:
    def get_cart_items(user_id):
        try:
            # Converter user_id para UUID
            if isinstance(user_id, str):
                try:
                    user_id = uuid.UUID(user_id)
                except ValueError:
                    return jsonify({"error": "ID de usuário inválido"}), 400
            
            results = (
                db.session.query(Cart, CartItems)
                .outerjoin(CartItems, Cart.id == CartItems.cart_id)
                .filter(Cart.user_id == user_id)
                .all()
            )

            if not results:
                return jsonify({"message": "Nenhum carrinho encontrado."}), 404

            carts_dict = {}

            for cart, item in results:
                if cart.id not in carts_dict:
                    carts_dict[cart.id] = {
                        "id": str(cart.id),  # Converter UUID para string
                        "user_id": str(cart.user_id),  # Converter UUID para string
                        "created_at": cart.created_at.isoformat() if cart.created_at else None,
                        "items": []
                    }
                if item:
                    carts_dict[cart.id]["items"].append({
                        "id": item.id,
                        "product_id": str(item.product_id) if item.product_id else None,
                        "product_name": item.product_name,
                        "product_price": str(item.product_price) if item.product_price else None,
                        "product_image": item.product_image,
                        "quantity": item.quantity,
                        "product_height": item.product_height,
                        "product_width": item.product_width,
                        "product_weight": item.product_weight,
                        "product_length": item.product_length,
                        "variations": item.variation_data
                    })

            return jsonify(list(carts_dict.values())), 200

        except Exception as e:
            print(f"Erro ao buscar carrinho: {e}")
            return jsonify({"error": "Erro interno do servidor"}), 500

    

    def add_cart(user_id, product, variations, quantity=1):
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
            variations = variations,
            quantity = quantity,
            
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
            "variation_data": cart_item.variation_data,
            "quantity": cart_item.quantity,
            "created_at": cart_item.created_at.isoformat()
        }

        return jsonify({'msg': 'Item adicionado ao carrinhjo', "items": item_data})
    
    

