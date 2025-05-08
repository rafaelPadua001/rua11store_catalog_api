from flask import Blueprint
from controllers.stockController import StockController
from flask_cors import CORS
import os

stock_bp = Blueprint("stock", __name__)

CORS(stock_bp, resources={r"/stock/*": {"origins": "*"}}, supports_credentials=True)

@stock_bp.route("/", methods=["GET"], strict_slashes=False)
def get_produtos():
    return StockController.get_stock()

@stock_bp.route("/", methods=["POST"], strict_slashes=False)
def post_produto():
    return StockController.create_stock()

@stock_bp.route("/<int:stock_id>", methods=["GET"], strict_slashes=False)
def get_produto_by_id(stock_id):
    return StockController.get_stock_by_id(stock_id)

@stock_bp.route("/<int:stock_id>", methods=["PUT"], strict_slashes=False)
def update_product(stock_id):
    return StockController.update_stock(stock_id)

@stock_bp.route("/<int:stock_id>", methods=["DELETE"], strict_slashes=False)
def delete_product(stock_id):
    return StockController.delete_stock(stock_id)
