import cloudinary
import cloudinary.uploader
import os
import json
from flask import jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from database import db
from models.product import Product
from models.stock import Stock
from controllers.productSeoController import ProductSeoController
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from decimal import Decimal, ROUND_HALF_UP
from controllers.productImageController import ProductImageController
from controllers.productVideoController import ProductVideoController
from controllers.variationController import VariationController
from models.productImage import ProductImage
from models.comment import Comment
from models.productSeo import ProductSeo
from models.variation import Variation

from datetime import datetime

class ProductController:
    UPLOAD_FOLDER = "uploads/product_images"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    @staticmethod
    def allowed_file(filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ProductController.ALLOWED_EXTENSIONS

    @staticmethod
    def formatar_nome(nome):
        return secure_filename(nome.replace(" ", "_"))

    @staticmethod
    def allowed_file(filename):
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def upload_imagem(imagem, product_name):
        if imagem and ProductController.allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            unique_id = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
            public_id = f"{filename.rsplit('.', 1)[0]}_{unique_id}"  # nome sem extensão
            
            try:
                upload_result = cloudinary.uploader.upload(
                    imagem,
                    folder=f'product_images/{product_name}',
                    public_id=public_id,
                    overwrite=False,
                    resource_type='image'
                )
                return upload_result.get("secure_url")
            except Exception as e:
                print(f"Erro ao fazer upload para o Cloudinary: {str(e)}")
                return None
        return None
    
    @staticmethod
    def allowed_video(filename):
        allowed_extensions = {"mp4", "mov", "avi", "mkv", "webm"}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    
    @staticmethod
    def upload_video(video_file, product_name):
        """
        Faz upload de um arquivo de vídeo para o Cloudinary e retorna a URL segura.
        """
        if not video_file or not ProductController.allowed_video(video_file.filename):
            return None
        
        ext = video_file.filename.rsplit('.', 1)[1].lower()
        public_id = secure_filename(f"{product_name}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}")
        
        try:
            upload_result = cloudinary.uploader.upload(
                video_file,
                folder=f"product_videos/{product_name}",
                public_id=public_id,
                resource_type="video",
                overwrite=True
            )
            return upload_result.get("secure_url")
        except Exception as e:
            print(f"Erro ao fazer upload de vídeo para o Cloudinary: {e}")
            return None

    @staticmethod
    def serve_uploaded_file(filename):
        return send_from_directory(ProductController.UPLOAD_FOLDER, filename)

    @staticmethod
    def listar_produtos():
        products = Product.get_all()
        return jsonify([
            {
                **item['product'],
                'product_quantity': item['product_quantity'],
                'thumbnail_path': (
                    # Novo campo principal
                    item['product'].get('thumbnail_path')
                    # Primeira imagem registrada em product_images
                    or (item.get('product_images')[0]['image_path']
                        if item.get('product_images') else None)
                    # Compatibilidade com campo antigo image_paths na tabela products
                    or (
                        item['product'].get('image_paths')[0]
                        if isinstance(item['product'].get('image_paths'), list)
                        and item['product'].get('image_paths') else None
                    )
                ),

                'seo': item.get('seo'),
                'images': item.get('product_images', []),  # adiciona as imagens aqui
                'video': (
                    item.get('product_videos', [])[0] 
                    if item.get('product_videos') 
                    else None
                ),

                'comments': [
                    comment for comment in item.get('comments', [])
                    if comment.get('product_id') == item['product']['id']
                ],
               
            }
            for item in products
        ])

    @staticmethod
    def get_by_slug(slug):
        data, error, status = ProductSeoController.get_by_slug(slug)

        if error:
            return jsonify(error), status

        product_data = data["product"]
        seo_data = data["seo"]

        #found relation images
        product_id = product_data['id']
        images = ProductImage.query.filter_by(product_id=product_id).all()
        comments = Comment.query.filter_by(product_id=product_id).all()
        variations = Variation.query.filter_by(product_id=product_id).all()
        image_list = [
            {
                "id": img.id,
                "url": img.image_path
            }
            for img in images
        ]

        comments_list = [
            {
                "id": comment.id,
                "comment": comment.comment,
                "userId": comment.user_id,
                "user_name": comment.user_name,
                "avatar_url": comment.avatar_url,
                "product_id": comment.product_id,
                "status": comment.status,
                "updated_at": comment.updated_at
            }
            for comment in comments
        ]

        variations_list = [
            {
                "id": variation.id,
                "product_id": variation.product_id,
                "product_name": variation.product_name,
                "variation_type": variation.variation_type,
                "value": variation.value,
                "quantity": variation.quantity,
            }

            for variation in variations
        ]

        return jsonify({
            "id": product_data["id"],
            "name": product_data["name"],
            "price": product_data["price"],
            "image_url": product_data['image_url'],
            "thumbnail_path": product_data['thumbnail_path'],
            "product_quantity": product_data.get("quantity", None),
            "description": product_data.get('description'),
            "seo": {
                "slug": seo_data["slug"],
                "meta_title": seo_data["meta_title"],
                "meta_description": seo_data["meta_description"],
                "meta_keywords": seo_data['meta_keywords'] 
            },
            "images": image_list,
            "comments": comments_list,
            "variations": variations_list,
            # Se quiser os comentários, precisa buscá-los separadamente
            # Ou incluir na consulta original
            # "comments": [...]
        })

    @staticmethod
    @jwt_required()
    def adicionar_produto():
        def to_float(value, default=0.0):
            try:
                return float(value)
            except (ValueError, TypeError):
                return default

        # Dados básicos
        raw_price = request.form.get("price", "0.00")
        price_decimal = Decimal(raw_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        name = request.form.get("name")
        description = request.form.get("description")
        price = float(price_decimal)
        category_id = int(request.form.get("category_id", 0))
        subcategory_id = int(request.form.get("subcategory_id", 0))
        quantity = int(request.form.get("quantity", 1))

        # Arquivos
        thumbnail_file = request.files.get("thumbnail")
        images_files = request.files.getlist("images")
        video_file = request.files.get("video")
        product_name = ProductController.formatar_nome(name) if name else "produto_sem_nome"

        thumbnail_path = ProductController.upload_imagem(thumbnail_file, product_name) if thumbnail_file else None
        imagem_paths = [ProductController.upload_imagem(img, product_name) for img in images_files if img] if images_files else []
        video_path = ProductController.upload_video(video_file, product_name) if video_file else None

        width = to_float(request.form.get("width"))
        height = to_float(request.form.get("height"))
        weight = to_float(request.form.get("weight"))
        length = to_float(request.form.get("length"))

        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"erro": "Usuário não autenticado"}), 401

        try:
            # 1️⃣ Adiciona produto na sessão (sem commit)
            novo_produto = Product(
                name=name,
                description=description,
                price=price,
                category_id=category_id,
                subcategory_id=subcategory_id,
                thumbnail_path=thumbnail_path,
                image_paths=imagem_paths,
                quantity=quantity,
                width=width,
                height=height,
                weight=weight,
                length=length,
                user_id=user_id
            )
            db.session.add(novo_produto)
            db.session.flush()  # força geração do ID

            # 2️⃣ Criar estoque
            stock_data = {
                "id_product": novo_produto.id,
                "user_id": novo_produto.user_id,
                "category_id": novo_produto.category_id,
                "product_name": novo_produto.name,
                "product_price": float(novo_produto.price),
                "product_quantity": novo_produto.quantity,
                "variations": None,
            }
            Stock.create(stock_data)

            # 3️⃣ Criar SEO
            seo_data = {
                "product_id": novo_produto.id,
                "meta_title": request.form.get("meta_title", ""),
                "meta_description": request.form.get("meta_description", ""),
                "slug": request.form.get("slug", ProductController.formatar_nome(name)),
                "keywords": request.form.get("keywords", "")
            }

            if any(seo_data.values()):
                seo = ProductSeo(**seo_data)
                novo_produto.seo = seo
                db.session.add(seo)

            # 4️⃣ Criar variações
            raw_sizes = request.form.get('sizes', '[]')
            raw_colors = request.form.get('colors', '[]')
            sizes = json.loads(raw_sizes) if raw_sizes else []
            colors = json.loads(raw_colors) if raw_colors else []

            variations = [
                {"type": "Size", "value": s.get("value"), "quantity": s.get("quantity", 0)}
                for s in sizes
            ] + [
                {"type": "Color", "value": c.get("value"), "quantity": c.get("quantity", 0)}
                for c in colors
            ]

            for v in variations:
                v['product_id'] = novo_produto.id
                v['product_name'] = novo_produto.name

            if variations:
                VariationController.insert_variations(
                    product_id=novo_produto.id,
                    product_name=novo_produto.name,
                    variations_data=variations
                )

            # 5️⃣ Salvar imagens extras
            if imagem_paths:
                ProductImageController.create_images(novo_produto.id, imagem_paths)

            # 6️⃣ Salvar vídeo
            if video_path:
                ProductVideoController.create_video(novo_produto.id, video_path)

            # 7️⃣ Commit de tudo de uma vez
            db.session.commit()

            return jsonify({
                "mensagem": "Produto adicionado com sucesso!",
                "product": novo_produto.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"erro": f"Erro ao adicionar produto: {str(e)}"}), 500


    @staticmethod
    @jwt_required()
    def update_product_data(product_id):
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"erro": "Usuário não autenticado"}), 401

        product = Product.find_by_id_and_user(product_id, user_id)
        if not product:
            return jsonify({"erro": "Produto não encontrado ou sem permissão"}), 404

        # Dados básicos
        name = request.form.get("name", product.name)
        description = request.form.get("description", product.description)
        price = request.form.get("price", product.price)
        category_id = request.form.get("category_id", product.category_id)
        subcategory_id = request.form.get("subcategory_id", product.subcategory_id)
        quantity = request.form.get("quantity", product.quantity)

        width = request.form.get('width', product.width)
        height = request.form.get('height', product.height)
        weight = request.form.get('weight', product.weight)
        length = request.form.get('length', product.length)

        # Campos de SEO
        meta_title = request.form.get("meta_title")
        meta_description = request.form.get("meta_description")
        slug = request.form.get("slug")
        keywords = request.form.get("keywords")

        # --------------------------
        # IMAGENS
        # --------------------------
        images = request.files.getlist("images")
        if images and any(img.filename for img in images):
            image_paths = []
            for img in images:
                if img and img.filename:
                    url = ProductController.upload_imagem(img, name)
                    if url:
                        image_paths.append(url)
            if image_paths:
                ProductImageController.update_images(product.id, image_paths)
        else:
            # Mantém as imagens já salvas
            image_paths = [img.image_path for img in getattr(product, "product_images", [])]

        # --------------------------
        # THUMBNAIL
        # --------------------------
        thumbnail = request.files.get('thumbnail')
        if thumbnail and thumbnail.filename and ProductController.allowed_file(thumbnail.filename):
            thumbnail_path = ProductController.upload_imagem(thumbnail, name)
        else:
            thumbnail_path = product.thumbnail_path

        # --------------------------
        # VÍDEO
        # --------------------------
        video = request.files.get('video')
        video_record = ProductVideoController.get_video_by_product(product.id)

        if video and video.filename and ProductController.allowed_video(video.filename):
            new_video_path = ProductController.upload_video(video, name)
            if video_record:
                ProductVideoController.update_video(product.id, new_video_path)
            else:
                ProductVideoController.create_video(product.id, new_video_path)
        else:
            # Mantém o vídeo já existente
            new_video_path = video_record.video_path if video_record else None

         # --------------------------
        # VARIAÇÕES (Size / Color)
        # --------------------------
       
        raw_sizes = request.form.get("sizes", "[]")
        raw_colors = request.form.get("colors", "[]")

        try:
            sizes = json.loads(raw_sizes)
            colors = json.loads(raw_colors)
        except:
            sizes = []
            colors = []

        variations = []

        for s in sizes:
            if s.get("value"):
                variations.append({
                    "type": "Size",
                    "value": s.get("value"),
                    "quantity": int(s.get("quantity", 0)),
                    "product_id": product.id,
                    "product_name": product.name
                })

        for c in colors:
            if c.get("value"):
                variations.append({
                    "type": "Color",
                    "value": c.get("value"),
                    "quantity": int(c.get("quantity", 0)),
                    "product_id": product.id,
                    "product_name": product.name
                })

        # Se enviou variações → apaga e insere de novo
        if variations:
            VariationController.delete_variations_by_product(product.id)
            VariationController.insert_variations(
                product_id=product.id,
                product_name=product.name,
                variations_data=variations
            )


        # --------------------------
        # ATUALIZA PRODUTO
        # --------------------------
        try:
            product.update(
                name=name,
                description=description,
                price=price,
                category_id=category_id,
                subcategory_id=subcategory_id,
                quantity=quantity,
                width=width,
                height=height,
                weight=weight,
                length=length,
                image_paths=image_paths,
                thumbnail_path=thumbnail_path
                # Se quiser salvar vídeo direto no produto, adicionar aqui:
                # video_path=new_video_path
            )

            # Estoque
            stock_data = {
                "id_product": product.id,
                "user_id": user_id,
                "category_id": product.category_id,
                "product_name": product.name,
                "product_price": float(product.price),
                "product_quantity": product.quantity,
                "product_width": product.width,
                "product_height": product.height,
                "product_weight": product.weight,
                "product_lenght": product.length,
                "variations": {
                    "sizes": [
                        {"value": v.value, "quantity": v.quantity}
                        for v in product.variations
                        if v.variation_type == 'Size'
                    ],
                    "colors": [
                        {"value": v.value, "quantity": v.quantity}
                        for v in product.variations
                        if v.variation_type == 'Color'
                    ]
                },
            }

            stock_id = Stock.get_stock_id_by_product(product.id)
            if stock_id:
                Stock.update(stock_id, stock_data)

            # SEO
            if any([meta_title, meta_description, slug, keywords]):
                seo_data = {
                    "meta_title": meta_title or product.meta_title,
                    "meta_description": meta_description or product.meta_description,
                    "slug": slug or product.slug,
                    "keywords": keywords or product.keywords
                }
                ProductSeoController.update_product_seo(product.id, seo_data)

            updated_product = Product.get_by_id(product.id)

            return jsonify({"mensagem": "Produto atualizado com sucesso!", "product": updated_product.to_dict()}), 200

        except Exception as e:
            return jsonify({"erro": f"Erro ao atualizar produto: {str(e)}"}), 500


    @staticmethod
    @jwt_required()
    def delete_product(product_id):
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"erro": "Usuário não autenticado"}), 401

        product = Product.find_by_id_and_user(product_id, user_id)
        if not product:
            return jsonify({"erro": "Produto não encontrado ou sem permissão"}), 404

        try:
            try:
                ProductImageController.delete_image_by_product(product.id)
            except Exception as e:
                print(f'Erro ao excluir imagens do produto: {str(e)}')
            try:
                ProductVideoController.delete_video_by_product(product.id)
            except Exception as e:
                print(f'Erro ao excluir vídeo do produto: {str(e)}')
            try:
                Stock.delete_by_productId(product.id)
            except Exception as e:
                print(f'Erro ao excliur do estoque: {str(e)}')    
            try:
                VariationController.delete_variations_by_product(product.id)
            except Exception as e:
                print(f'Erro ao excluir variações: {str(e)}')
            product.delete()
            return jsonify({"mensagem": "Produto excluído com sucesso"}), 200
        except Exception as e:
            return jsonify({"erro": f"Erro ao excluir produto: {str(e)}"}), 500