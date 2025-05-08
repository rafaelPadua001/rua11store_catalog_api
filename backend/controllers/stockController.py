from flask import jsonify, request
from models.stock import Stock
from controllers.productController import ProductController 


class StockController:
    @staticmethod
    def create_stock():
        data = request.get_json() 
        if not data:
            return jsonify({"error": "Dados inválidos"}), 400

        stock_id = Stock.create(data)
        return jsonify({"message": "Item criado com sucesso!", "id": stock_id}), 201

    @staticmethod
    def get_stock():
        stocks = Stock.get_all()
        stocks_list = [dict(row) for row in stocks]  
        return jsonify(stocks_list), 200

    @staticmethod
    def get_stock_by_id(stock_id):  
        stock = Stock.get_by_id(stock_id)
        if stock:
            return jsonify(stock), 200
        
        return jsonify({"error": "Item não encontrado!"}), 404

    @staticmethod
    def update_stock(stock_id):
        data = request.get_json()  
        if not data:
            return jsonify({"error": "Dados inválidos"}), 400

        updated = Stock.update(stock_id, data)
        if updated:
            return jsonify({"message": "Item atualizado com sucesso!"}), 200 

        return jsonify({"error": "Item não encontrado"}), 404
    
    @staticmethod
    def update_stock_quantity(stock_id):
        
        stock_item = Stock.get_by_id(stock_id)
        if not stock_item:
            
            return jsonify({"error": "Item de estoque não encontrado"}), 404

        stock_dict = dict(stock_item)
        updated_quantity = Stock.update_stock_quantity(stock_id, 1)
        if updated_quantity:
            return jsonify({"message": "Quantidade de estoque atualizada com sucesso", "stock_id": stock_dict}), 200
            
    @staticmethod
    def delete_stock(stock_id): 
        stock_item = Stock.get_by_id(stock_id)
        if not stock_item:
            jsonify({"error": "Item não encontrado"}), 404

        product_id = stock_item.product_id
        
        deleted = Stock.delete(stock_id)
        if deleted:
            # ProductController.delete_product(stock_id)
            return jsonify({"message": "Item removido com sucesso"}), 200  
        
        return jsonify({"error": "Item não encontrado"}), 404
