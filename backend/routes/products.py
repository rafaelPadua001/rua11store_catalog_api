from flask import Blueprint, request
from controllers.productController import listar_produtos, adicionar_produto, update_product_data
from flask_cors import CORS

products_bp = Blueprint("products", __name__)

CORS(products_bp, resources={r"/products/*": {"origins": "*"}}, supports_credentials=True)



@products_bp.route("/", methods=["GET"], strict_slashes=False)
def get_produtos():
    return listar_produtos()

@products_bp.route("/", methods=["POST"], strict_slashes=False)
def post_produto():
    return adicionar_produto()

@products_bp.route('/<int:product_id>', methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def update_product(product_id):
   if(request.method == 'PUT'):
        return update_product_data(product_id)
