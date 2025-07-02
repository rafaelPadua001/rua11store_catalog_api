from flask import Blueprint, request
from controllers.productSeoController import ProductSeoController

product_seo_bp = Blueprint('product_seo', __name__)

@product_seo_bp.route('/product-seo', methods=['POST'])
def create_product_seo():
    data = request.get_json()
    return ProductSeoController.create_product_seo(data)