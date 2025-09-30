from flask import Flask, render_template_string, redirect
from sqlalchemy.orm import joinedload
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
            seo = post.seo_metadata
            comments = [c.to_dict() for c in post.comments]
            views = [v.to_dict() for v in post.views]
            result.append({
                 "id": post.id,
                "page_id": post.page_id,
                "slug": post.slug,
                "title": post.title,
                "excerpt": post.excerpt,
                "content": post.content,
                "cover_image": post.cover_image,
                "created_at": post.created_at,
                "updated_at": post.updated_at,
                "seo": seo.to_dict() if seo else None,
                "comments": comments,
                "views": views
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
                # Nome do blog vai ser usado como pasta no Cloudinary
                blog_folder = f"blogs/{post.slug or post.title.replace(' ', '_')}"
                
                upload_result = cloudinary_upload(
                    cover_image,
                    folder=blog_folder,
                    public_id="cover",  # nome fixo (cover.jpg) dentro da pasta
                    overwrite=True,
                    resource_type="image"
                )
                
                # Pega a URL segura do Cloudinary
                post.cover_image = upload_result.get("secure_url")

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
                result = cloudinary_upload(cover_image)
                post.cover_image = result.get("secure_url")
            else:  # já é uma URL
                post.cover_image = cover_image

        post.updated_at = datetime.utcnow()
        db.session.commit()

        # Atualizar SEO, se vier dados de SEO junto
        seo_data = {
            "keywords": data.get("keywords"),
            "description": data.get("description"),
            "canonical_url": data.get("canonical_url"),
            "og_title": data.get("og_title"),
            "og_description": data.get("og_description"),
            "og_image": data.get("og_image"),
        }

        if any(seo_data.values()):  # só chama se tiver algum dado de SEO
            PostSeoController.update_seo(post.id, seo_data)

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
    def share_post(slug):
        try:
            # Remove parâmetros da URL se existirem
            clean_slug = slug.split('?')[0]
            print(f"📋 Tentando encontrar post com slug: {clean_slug}")  # DEBUG
            
            post = BlogPost.query.filter_by(slug=slug).first_or_404()
            print(f"✅ Post encontrado: {post.title}")  # DEBUG
            
            title = post.title or "Rua11Store Blog"
            description = post.excerpt or "Confira este artigo no blog Rua11Store!"
            image = post.cover_image or "https://res.cloudinary.com/dnfnevy9e/image/upload/v1758308180/cratlzxc3sf2qxelqru8.png"
            
            # URL do FRONTEND (onde o post realmente está)
            frontend_url = f"https://rua11store-catalog-api.vercel.app/blog/blogView/{post.slug}"
            current_url = f"https://rua11store-catalog-api-lbp7.onrender.com/blog/share/{clean_slug}"

            html = f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="utf-8">
                <title>{title}</title>
                <link rel="canonical" href="{frontend_url}" />

                <!-- Open Graph -->
                <meta property="og:title" content="{title}" />
                <meta property="og:description" content="{description}" />
                <meta property="og:image" content="{image}" />
                <meta property="og:image:width" content="1200" />
                <meta property="og:image:height" content="630" />
                <meta property="og:url" content="{frontend_url}" />
                <meta property="og:type" content="article" />
                <meta property="og:site_name" content="Rua11Store Blog" />
                <meta property="fb:app_id" content="801771992806957" />
            </head>
            <body>
                <script>
                    window.location.href = "{frontend_url}";
                </script>
                <p>Redirecionando para <a href="{frontend_url}">{title}</a></p>
            </body>
            </html>
            """
            return html, 200, {"Content-Type": "text/html"}
            
        except Exception as e:
            print(f"❌ ERRO em share_post: {e}")  # DEBUG
            print(f"❌ Slug recebido: {slug}")  # DEBUG
            # Fallback em caso de erro
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Artigo do Blog Rua11Store</title>
                <meta property="og:title" content="Rua11Store Blog" />
                <meta property="og:description" content="Confira nossos artigos!" />
                <meta property="og:image" content="https://res.cloudinary.com/dnfnevy9e/image/upload/v1758308180/cratlzxc3sf2qxelqru8.png" />
                <meta property="og:url" content=https://rua11store-catalog-api.vercel.app/blog/blogView/{post.slug}" />
            </head>
            <body>
                <p>Visite nosso blog: <a href="https://rua11store-catalog-api.vercel.app/blog/blogView/{post.slug}">Rua11Store Blog</a></p>
            </body>
            </html>
            """
            return html, 200, {"Content-Type": "text/html"}



    @staticmethod
    def delete_post(post_id):
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deletado com sucesso"}), 200
