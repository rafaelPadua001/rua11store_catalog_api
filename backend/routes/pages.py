from flask import Blueprint, jsonify, request
from controllers.pageController import PageController

pages_bp = Blueprint('pages', __name__)

@pages_bp.route("/pages", methods=["GET"])
def list_pages():
    pages = PageController.get_all_pages()
    return jsonify({"pages": pages}), 200

@pages_bp.route("/pages", methods=["POST", "OPTIONS"])
def create_page():
    if request.method == 'OPTIONS':
        return '', 204  # responde ao preflight
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    data = request.get_json()

    PageController.create_page(data)
    return jsonify({'message': 'Page created'}), 201