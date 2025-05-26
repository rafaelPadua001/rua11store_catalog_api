from flask import Blueprint, jsonify, request
from controllers.pageController import PageController

pages_bp = Blueprint('pages', __name__)

@pages_bp.route("/pages", methods=["GET"])
def list_pages():
    pages = PageController.get_all_pages()
    return jsonify({"pages": pages}), 200

@pages_bp.route("/pages/<int:page_id>", methods=["GET"])
def get_page(page_id):
    page = PageController.get_page_by_id(page_id)
    if page:
        return jsonify({
            "id": page.id,
            "title": page.title,
            "content": page.content}), 200
    else:
        return jsonify({"error": "Page not found"}), 404
    
@pages_bp.route("/pages/<string:page_name>", methods=["GET"])
def get_page_name(page_name):
    print(page_name)
    page = PageController.get_page_by_name(page_name)
    if page:
        return jsonify({
            "id": page.id,
            "title": page.title,
            "content": page.content
        }), 200
    else:
        return jsonify({"error": "Página não encontrada"}), 404

@pages_bp.route("/pages", methods=["POST", "OPTIONS"])
def create_page():
    if request.method == 'OPTIONS':
        return '', 204  # responde ao preflight
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    data = request.get_json()

    PageController.create_page(data)
    return jsonify({'message': 'Page created', "page": data}), 200

@pages_bp.route("/pages/<int:page_id>", methods=["PUT"])
def update_page(page_id):
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    data = request.get_json()

    PageController.update_page(page_id, data)
    return jsonify({'message': 'Page updated', "page": data}), 200

@pages_bp.route("/pages/<int:page_id>", methods=["DELETE"])
def delete_page(page_id):
    PageController.delete_page(page_id)
    return jsonify({'message': 'Page deleted'}), 200