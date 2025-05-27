from flask import Blueprint, jsonify, request
from controllers.seoController import SeoController

seo_bp = Blueprint('seo', __name__)
@seo_bp.route('/seo', methods=['GET'])
def list_seo():
    seo = SeoController.get_all_seo()
    return jsonify({"seo": seo}), 200

@seo_bp.route('/seo/<int:seo_id>', methods=['GET'])
def get_seo_by_id(seo_id):
    seo = SeoController.get_seo_by_id(seo_id)

    if  seo is None:
        return jsonify({"error": "SEO item not found"}), 404
    return jsonify({"seo": seo.to_dict()}), 200

@seo_bp.route('/seo', methods=['POST'])
def create_seo():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be a JSON object"}), 400
    required_fields = ['route', 'metaTitle', 'metaDescription', 'metaKeywords', 'ogTitle', 'ogDescription', 'ogImage']
    SeoController.save_seo(data)
    # Lógica para criar um novo item de SEO
    return jsonify({"message": "SEO item created", "seo": data}), 201

@seo_bp.route("/seo/<int:seo_id>", methods=["PUT"])
def update_seo(seo_id):
    data = request.get_json()
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be a JSON object"}), 400

    SeoController.update_seo(seo_id, data)
    return jsonify({'message': 'SEO item updated', "seo": data}), 200

@seo_bp.route("/seo/<int:seo_id>", methods=["DELETE"])
def delete_seo(seo_id):
    SeoController.delete_seo(seo_id)
    return jsonify({'message': 'SEO item deleted'}), 200