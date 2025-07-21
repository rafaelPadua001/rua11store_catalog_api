from controllers.productController import ProductController
from flask import Blueprint, request
from flask_cors import CORS
import os

products_bp = Blueprint("products", __name__)

CORS(products_bp, resources={r"/products/*": {"origins": "*"}}, supports_credentials=True)



@products_bp.route("/", methods=["GET"], strict_slashes=False)
def get_produtos():
    return ProductController.listar_produtos()

@products_bp.route("/", methods=["POST"], strict_slashes=False)
def post_produto():
    return ProductController.adicionar_produto()

@products_bp.route('/<int:product_id>', methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def update_product(product_id):
   if(request.method == 'PUT'):
        return ProductController.update_product_data(product_id)
   if(request.method == 'DELETE'):
       return ProductController.delete_product(product_id)

@products_bp.route('/product/<string:slug>', methods=["GET"])
def get_by_slug(slug):
    return ProductController.get_by_slug(slug)

@products_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # Ajuste o caminho conforme sua estrutura de diretórios
    uploads_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    return ProductController.send_from_directory(uploads_dir, filename)


