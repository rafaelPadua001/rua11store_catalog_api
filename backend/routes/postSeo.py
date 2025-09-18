from flask import Blueprint, request, jsonify
from database import db
from models.blogPost import BlogPost
from models.postSeo import PostSeo
from controllers.postSeoController import PostSeoController 

postSeo_bp = Blueprint("post-seo", __name__)

@postSeo_bp.route("/post_seo/<int:post_id>", methods=["POST", "PUT"])
def save_seo(post_id):
    return PostSeoController.save_seo(post_id)

@postSeo_bp.route("/post_seo/<int:post_id>", methods=["GET"])
def get_seo(post_id):
    seo = PostSeo.query.filter_by(post_id=post_id).first()
    if not seo:
        return jsonify({"error": "SEO não encontrado"}), 404

    return jsonify({
        "keywords": seo.keywords,
        "description": seo.description,
        "canonical_url": seo.canonical_url,
        "og_title": seo.og_title,
        "og_description": seo.og_description,
        "og_image": seo.og_image
    })
