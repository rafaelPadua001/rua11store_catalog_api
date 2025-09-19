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
  return PostSeoController.get_seo(post_id)
