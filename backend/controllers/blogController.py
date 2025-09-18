from models.blogPost import BlogPost
from models.page import Page
from controllers.postSeoController import PostSeoController
from database import db
from datetime import datetime
from flask import jsonify, request
from cloudinary.uploader import upload as cloudinary_upload

class BlogController:
    @staticmethod
    def get_posts():
        posts = BlogPost.query.all()
        result = []
        for post in posts:
            result.append({
                "id": post.id,
                "page_id": post.page_id,
                "slug": post.slug,
                "title": post.title,
                "excerpt": post.excerpt,
                "content": post.content,
                "cover_image": post.cover_image,
                "created_at": post.created_at,
                "updated_at": post.updated_at
            })
        return jsonify(result), 200
    
    @staticmethod
    def get_post_by_slug(slug):
        try:
            post = BlogPost.query.filter_by(slug=slug).first()

            if not post:
                return jsonify({"Error": "Post não encontrado"}), 404
            
            post_data = {
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
                "excerpt": post.excerpt,
                "content": post.content,
                "cover_image": post.cover_image,
                "created_at": post.created_at,
                "updated_at": post.updated_at,
            }

            return jsonify({"post": post_data}), 200
        except Exception as e:
            return jsonify({'Error': str((e))}), 500

    @staticmethod
    def create_post():
        try:
            data = request.form
            cover_image = request.files.get("cover_image")

            page_id = data.get("page_id")
            if not page_id:
                return jsonify({"error": "page_id é obrigatório"}), 400

            post = BlogPost(
                page_id=page_id,
                title=data.get("title"),
                slug=data.get("slug"),
                excerpt=data.get("excerpt"),
                content=data.get("content")
            )

            if cover_image:
                filename = f"uploads/{cover_image.filename}"
                cover_image.save(filename)
                post.cover_image = filename

            # Salva o post no banco
            db.session.add(post)
            db.session.commit()

            # Agora cria o SEO
            seo_data = {
                "keywords": data.get("keywords"),
                "description": data.get("description"),
                "canonical_url": data.get("canonical_url"),
                "og_title": data.get("og_title"),
                "og_description": data.get("og_description"),
                "og_image": data.get("og_image"),
            }

            PostSeoController.save_seo(post.id, seo_data)

            return jsonify({"post": {
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
                "excerpt": post.excerpt,
                "content": post.content,
                "cover_image": post.cover_image,
                "created_at": post.created_at
            }}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_post(post_id, data):
        post = BlogPost.query.get_or_404(post_id)

        post.slug = data.get('slug', post.slug)
        post.title = data.get('title', post.title)
        post.excerpt = data.get('excerpt', post.excerpt)
        post.content = data.get('content', post.content)

        # Caso venha arquivo de imagem
        cover_image = data.get('cover_image')
        if cover_image:
            if hasattr(cover_image, 'read'):  # é um arquivo
                result = cloudinary.uploader.upload(cover_image)
                post.cover_image = result.get("secure_url")
            else:  # já é uma URL
                post.cover_image = cover_image

        post.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "message": "Post atualizado com sucesso",
            "post": {
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
                "excerpt": post.excerpt,
                "content": post.content,
                "cover_image": post.cover_image,
                "updated_at": post.updated_at
            }
        }), 200

    @staticmethod
    def delete_post(post_id):
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deletado com sucesso"}), 200
