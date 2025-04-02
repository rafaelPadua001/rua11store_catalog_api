from flask import Blueprint, request, jsonify
from controllers.productController import listar_produtos, adicionar_produto
from flask_cors import CORS

products_bp = Blueprint("products", __name__)
CORS(products_bp, supports_credentials=True)  # Habilita CORS para este Blueprint

@products_bp.route("/products/", methods=["OPTIONS", "GET"])
def get_produtos():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    return listar_produtos()

@products_bp.route("/", methods=["OPTIONS", "POST"])
def post_produto():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    return adicionar_produto(request.json)

def _build_cors_preflight_response():
    """ Responde manualmente ao preflight request (OPTIONS) """
    response = jsonify({"message": "CORS Preflight OK"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response
