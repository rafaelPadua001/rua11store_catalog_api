from flask import jsonify, request
from models.stock import Stock


class StockController:
    @staticmethod
    def create_stock():
        data = request.get_json()  # ✅ Corrigido
        if not data:
            return jsonify({"error": "Dados inválidos"}), 400

        stock_id = Stock.create(data)
        return jsonify({"message": "Item criado com sucesso!", "id": stock_id}), 201

    @staticmethod
    def get_stock():
        stocks = Stock.get_all()
        stocks_list = [dict(row) for row in stocks]  # Converte cada Row para dicionário
        return jsonify(stocks_list), 200

    @staticmethod
    def get_stock_by_id(stock_id):  # ✅ Nome alterado para evitar conflito
        stock = Stock.get_by_id(stock_id)
        if stock:
            return jsonify(stock), 200
        
        return jsonify({"error": "Item não encontrado!"}), 404

    @staticmethod
    def update_stock(stock_id):
        data = request.get_json()  # ✅ Corrigido
        if not data:
            return jsonify({"error": "Dados inválidos"}), 400

        updated = Stock.update(stock_id, data)
        if updated:
            return jsonify({"message": "Item atualizado com sucesso!"}), 200  # ✅ Código 200 (OK)

        return jsonify({"error": "Item não encontrado"}), 404

    @staticmethod
    def delete_stock(stock_id):  # ✅ Corrigido erro de digitação
        deleted = Stock.delete(stock_id)
        if deleted:
            return jsonify({"message": "Item removido com sucesso"}), 200  # ✅ Código de status correto
        
        return jsonify({"error": "Item não encontrado"}), 404
