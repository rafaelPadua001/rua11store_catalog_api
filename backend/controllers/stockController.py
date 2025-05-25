import sqlite3
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
    def update_stock_quantity(product_id, quantity, conn=None):
        """Atualiza a quantidade de um item do estoque"""
        should_close = False
        if conn is None:
            conn = Stock.get_db_connection()
            should_close = True

        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(""" 
                SELECT product_quantity, id FROM stock WHERE id_product = ?
            """, (product_id,))
            row = cursor.fetchone()

            if row is None:
                return False
            
            current_quantity = row['product_quantity']
            new_quantity = current_quantity - quantity

            if new_quantity < 0:
                return {"error": "Quantidade insuficiente em estoque"}

            cursor.execute(
                "UPDATE stock SET product_quantity = ? WHERE id = ?",
                (new_quantity, row['id'])
            )

            return {
                "stock_id": row['id'],
                "old_quantity": current_quantity,
                "new_quantity": new_quantity
            }
        finally:
            if should_close:
                conn.close()


            
    @staticmethod
    def delete_stock(stock_id): 
        print(stock_id)
        stock_item = Stock.get_by_id(stock_id)
        if not stock_item:
            jsonify({"error": "Item não encontrado"}), 404

        #product_id = stock_item.product_id
        
        deleted = Stock.delete(stock_id)
        if deleted:
            # ProductController.delete_product(stock_id)
            return jsonify({"message": "Item removido com sucesso"}), 200  
        
        return jsonify({"error": "Item não encontrado"}), 404
