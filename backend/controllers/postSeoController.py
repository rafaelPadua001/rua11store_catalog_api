from flask import Blueprint, request, jsonify
from database import db
from models.blogPost import BlogPost
from models.postSeo import PostSeo

class PostSeoController:
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
    
    @staticmethod
    def update_seo(post_id, data):
        seo = PostSeo.query.filter_by(post_id=post_id).first()
        if not seo:
            return jsonify({"error": "SEO não encontrado"}), 404

        # Atualiza apenas os campos enviados
        if "keywords" in data: seo.keywords = data["keywords"]
        if "description" in data: seo.description = data["description"]
        if "canonical_url" in data: seo.canonical_url = data["canonical_url"]
        if "og_title" in data: seo.og_title = data["og_title"]
        if "og_description" in data: seo.og_description = data["og_description"]
        if "og_image" in data: seo.og_image = data["og_image"]

        seo.updated_at = db.func.now()

        db.session.commit()

        return jsonify({
            "message": "SEO atualizado com sucesso",
            "seo": {
                "keywords": seo.keywords,
                "description": seo.description,
                "canonical_url": seo.canonical_url,
                "og_title": seo.og_title,
                "og_description": seo.og_description,
                "og_image": seo.og_image,
                "updated_at": seo.updated_at
            }
        }), 200



