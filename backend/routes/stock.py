from flask import Blueprint, request
# from controllers.productController import listar_produtos, adicionar_produto, update_product_data, send_from_directory, delete_product
from flask_cors import CORS
import os

stock_bp = Blueprint("stock", __name__)

CORS(stock_bp, resources={r"/stock/*": {"origins": "*"}}, supports_credentials=True)



@stock_bp.route("/", methods=["GET"], strict_slashes=False)
def get_produtos():
    return listar_produtos()

@stock_bp.route("/", methods=["POST"], strict_slashes=False)
def post_produto():
    return adicionar_produto()

@stock_bp.route('/<int:product_id>', methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def update_product(product_id):
   if(request.method == 'PUT'):
        return update_product_data(product_id)
   if(request.method == 'DELETE'):
       return delete_product(product_id)

@stock_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # Ajuste o caminho conforme sua estrutura de diretórios
    uploads_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    return send_from_directory(uploads_dir, filename)


