from flask import jsonify, request
from models.stock import Stock
from controllers.productController import ProductController
from database import db  # sua instância do SQLAlchemy

class StockController:
    @staticmethod
    def create_stock():
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados inválidos"}), 400

        try:
            stock = Stock(**data)  # supõe que as chaves batem com colunas do model
            db.session.add(stock)
            db.session.commit()
            return jsonify({"message": "Item criado com sucesso!", "id": stock.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_stock():
        stocks = Stock.query.all()
        stocks_list = [stock.to_dict() for stock in stocks]  # to_dict deve estar no model
        return jsonify(stocks_list), 200

    @staticmethod
    def get_stock_by_id(stock_id):
        stock = Stock.query.get(stock_id)
        if stock:
            return jsonify(stock.to_dict()), 200
        return jsonify({"error": "Item não encontrado!"}), 404

    @staticmethod
    def update_stock(stock_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados inválidos"}), 400

        stock = Stock.query.get(stock_id)
        if not stock:
            return jsonify({"error": "Item não encontrado"}), 404

        try:
            for key, value in data.items():
                setattr(stock, key, value)
            db.session.commit()
            return jsonify({"message": "Item atualizado com sucesso!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_stock_quantity(product_id, quantity):
        stock = Stock.query.filter_by(id_product=product_id).first()
        if not stock:
            return jsonify({"error": "Item não encontrado"}), 404

        new_quantity = stock.product_quantity - quantity
        if new_quantity < 0:
            return jsonify({"error": "Quantidade insuficiente em estoque"}), 400

        try:
            stock.product_quantity = new_quantity
            db.session.commit()
            return jsonify({
                "stock_id": stock.id,
                "old_quantity": stock.product_quantity + quantity,
                "new_quantity": new_quantity
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def delete_stock(stock_id):
        stock = Stock.query.get(stock_id)
        if not stock:
            return jsonify({"error": "Item não encontrado"}), 404

        try:
            db.session.delete(stock)
            db.session.commit()
            # ProductController.delete_product(stock.product_id) # se quiser deletar produto também
            return jsonify({"message": "Item removido com sucesso"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
