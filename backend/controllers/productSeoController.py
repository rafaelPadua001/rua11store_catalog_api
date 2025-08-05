from flask import request, jsonify
from models.productSeo import ProductSeo
from database import db
from sqlalchemy.orm import joinedload

class ProductSeoController:
    @staticmethod
    def list_product_seo():
        produtos_seo = db.session.query(ProductSeo).all()
        result = []
        for p in produtos_seo:
            result.append({
                'slug': p.slug,
                # outros campos se precisar
            })
        return result
    
    @staticmethod
    def create_product_seo(data):
        required_fields = ['product_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        try:
            existing = ProductSeo.query.filter_by(product_id=data['product_id']).first()
            if existing:
                return jsonify({"error": "Product SEO already exists for this product"}), 400
            
            seo = ProductSeo(
                product_id=data['product_id'],
                meta_title=data.get('meta_title'),
                meta_description=data.get('meta_description'),
                slug=data.get('slug'),
                keywords=data.get('keywords')
            )

            db.session.add(seo)
            db.session.commit()

            return jsonify({'message': 'Product SEO created successfully', 'seo_id': seo.id}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def update_product_seo(product_id, seo_data):
        print("SEO form data recebida:", {
            "meta_title": request.form.get("meta_title"),
            "meta_description": request.form.get("meta_description"),
            "slug": request.form.get("slug"),
            "keywords": request.form.get("keywords")
        })

        try:
            seo = ProductSeo.query.filter_by(product_id=product_id).first()

            if not seo:
                # Se não existir, cria novo
                seo = ProductSeo(
                    product_id=product_id,
                    meta_title=seo_data.get("meta_title"),
                    meta_description=seo_data.get("meta_description"),
                    slug=seo_data.get("slug"),
                    keywords=seo_data.get("keywords")
                )
                db.session.add(seo)
            else:
                # Se já existir, atualiza
                seo.meta_title = seo_data.get("meta_title", seo.meta_title)
                seo.meta_description = seo_data.get("meta_description", seo.meta_description)
                seo.slug = seo_data.get("slug", seo.slug)
                seo.keywords = seo_data.get("keywords", seo.keywords)

            db.session.commit()
            return jsonify({"mensagem": "SEO atualizado com sucesso!"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": f"Erro ao atualizar SEO: {str(e)}"}), 500
        
    @staticmethod
    def get_by_slug(slug):
        try:
            seo = ProductSeo.query.options(joinedload(ProductSeo.product)).filter_by(slug=slug).first()

            if not seo:
                return None, {"error": "Slug não encontrado"}, 404

            product = seo.product

            if not product:
                return None, {"error": "Produto não encontrado"}, 404

            return {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "image_url": product.image_paths,
                    "thumbnail_path": product.thumbnail_path,
                    "quantity": product.quantity,
                    "description": product.description
                    # outros campos...
                },
                "seo": {
                    "slug": seo.slug,
                    "meta_title": seo.meta_title,
                    "meta_description": seo.meta_description,
                    "meta_keywords": seo.keywords
                }
            }, None, None

        except Exception as e:
            print(f'Erro ao buscar produto por slug: {e}')
            return None, {"error": "Erro interno"}, 500