from flask import jsonify
from models.cartItems import CartItems
from models.cart import Cart
from database import db

class CartItemController:
    def add_cart_item(cart_id, user_id, product, quantity=1):
        # create cart item
        cart_item = CartItems(
            cart_id = cart_id,
            product_id = product.id,
            user_id = user_id,
            product_name = product.name,
            product_price = product.price,
            product_image = product.thumbnail_path,
            product_height = product.height,
            product_width = product.width,
            product_weight = product.weight,
            product_length = product.length,
            quantity = quantity

        )

        db.session.add(cart_item)
        db.session.commit()

        return cart_item
    
    def remove_item_cart(itemId):
        item = CartItems.query.get(itemId)
        
        if not item:
            return jsonify({'message': "Item não encontrado"}), 404
        
        try:
            db.session.delete(item)
            db.session.commit()

            return jsonify({'message': 'Item removido com sucesso.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"Erro ao remve item: {str(e)}"}), 500