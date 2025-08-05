from flask import Blueprint, request, jsonify
from controllers.productSeoController import ProductSeoController

product_seo_bp = Blueprint('product_seo', __name__)

@product_seo_bp.route('/product-seo', methods=['POST'])
def create_product_seo():
    data = request.get_json()
    return ProductSeoController.create_product_seo(data)

@product_seo_bp.route('/', methods=['GET'])
def list_product_seo():
    # Aqui deve retornar a lista de produtos com slug para o sitemap
    produtos = ProductSeoController.list_product_seo()
    return jsonify(produtos)
