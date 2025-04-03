from flask import jsonify, request
from models.stock import Stock

class StockController:
    @staticmethod
    def create_stock():
        data = request.json()
        if not data: 
            return jsonify({"error": "Dados inválidos"}), 400
        
        stock_id = Stock.create(data)
        return jsonify({"message": "Item criado com sucesso !", "id": stock_id}), 201
    
    @staticmethod
    def get_stock():
        stocks = Stock.get_all()
        return jsonify(stocks), 200
    
    @staticmethod
    def get_stock(stock_id):
        stock = Stock.get_by_id(stock_id)
        if stock:
            return jsonify(stock), 200
        
        return jsonify({"error": "Item não encontrado !"}), 404
    
    @staticmethod
    def update_stock(stock_id):
        data = request.json()
        if not data:
            return jsonify({"error": "Dados inválidos"}), 404
        
        updated = Stock.update(stock_id, data)
        if updated:
            return jsonify({"message": "Item atualizado com sucesso !"}), 400
        
        return jsonify({"error": "Item não encontrado"}), 404
    
    @staticmethod
    def detele_stock(stock_id):
        deleted = Stock.delete(stock_id)
        if deleted:
            return jsonify({"message": "Item removido com sucesso"})
        
        return jsonify({"error": "Item não encontrado"}), 404