from models.blogPost import BlogPost
from models.page import Page
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
            title = request.form.get("title")
            slug = request.form.get("slug")
            content = request.form.get("content")
            excerpt = request.form.get("excerpt")
            page_id = request.form.get("page_id")

            if not all([title, slug, content, page_id]):
                return jsonify({"error": "Campos obrigatórios faltando"}), 400

            cover_image_url = None
            if "cover_image" in request.files:
                image_file = request.files["cover_image"]
                result = cloudinary_upload(image_file, folder="blog_posts")
                cover_image_url = result.get("secure_url")

            post = BlogPost(
                title=title,
                slug=slug,
                excerpt=excerpt,
                content=content,
                page_id=int(page_id),
                cover_image=cover_image_url
            )

            db.session.add(post)
            db.session.commit()

            return jsonify({
                "message": "Post criado com sucesso!",
                "post": {
                    "id": post.id,
                    "title": post.title,
                    "slug": post.slug,
                    "cover_image": post.cover_image
                }
            }), 201

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
