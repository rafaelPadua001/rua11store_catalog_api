from flask import Blueprint, request, jsonify
from database import db
from models.blogPost import BlogPost
from models.postSeo import PostSeo

class PostSeoController:
    @staticmethod
    def save_seo(post_id, data):
        seo = PostSeo.query.filter_by(post_id=post_id).first()
        if not seo:
            seo = PostSeo(post_id=post_id)

        seo.keywords = data.get("keywords")
        seo.description = data.get("description")
        seo.canonical_url = data.get("canonical_url")
        seo.og_title = data.get("og_title")
        seo.og_description = data.get("og_description")
        seo.og_image = data.get("og_image")

        db.session.add(seo)
        db.session.commit()
        return seo

    
    
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



