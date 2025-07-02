import os
from flask import jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from database import db
from models.product import Product
from models.stock import Stock
from controllers.productSeoController import ProductSeoController
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from decimal import Decimal, ROUND_HALF_UP
import cloudinary
import cloudinary.uploader

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
    def upload_imagem(imagem, product_name):
        if imagem and ProductController.allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)

            # upload to cloudinary
            try:
                upload_result = cloudinary.uploader.upload(
                    imagem,
                    folder=f'product_images/{product_name}', #create folder to cloudinary
                    public_id=filename.rsplit('.', 1)[0], # create name without extensions 
                    overwrite=True,
                    resource_type='image'
                )

                return upload_result.get("secure_url", None)
                
            except Exception as e:
                print(f"Erro ao fazer upload para o Cloudinary: {str(e)}")
                return None
            

            # upload to local storage
            #product_folder = os.path.join(ProductController.UPLOAD_FOLDER, product_name)
            #os.makedirs(product_folder, exist_ok=True)
            #filepath = os.path.join(product_folder, filename)
            #imagem.save(filepath)
            #return filepath
        return None

    @staticmethod
    def serve_uploaded_file(filename):
        return send_from_directory(ProductController.UPLOAD_FOLDER, filename)

    @staticmethod
    def listar_produtos():
        products = Product.get_all()
        return jsonify([
            {**item['product'].to_dict(), 'product_quantity': item['product_quantity']}
            for item in products
        ])

    @staticmethod
    @jwt_required()
    def adicionar_produto():
        raw_price = request.form.get("price", "0.00")
        price_decimal = Decimal(raw_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        name = request.form.get("name")
        description = request.form.get("description")
        price = float(price_decimal)
        category_id = int(request.form.get("category_id", 0))
        subcategory_id = int(request.form.get("subcategory_id", 0))
        quantity = int(request.form.get("quantity", 1))
        imagem = request.files.get("imagem")
        product_name = ProductController.formatar_nome(name) if name else "produto_sem_nome"
        imagem_path = ProductController.upload_imagem(imagem, product_name) if imagem else None
        width = float(request.form.get("width", 0))
        height = float(request.form.get("height", 0))
        weight = float(request.form.get("weight", 0))
        length = float(request.form.get("length", 0))

        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"erro": "Usuário não autenticado"}), 401

        try:
            novo_produto = Product(
                name=name,
                description=description,
                price=price,
                category_id=category_id,
                subcategory_id=subcategory_id,
                image_path=imagem_path,
                quantity=quantity,
                width=width,
                height=height,
                weight=weight,
                length=length,
                user_id=user_id

            )
            novo_produto.save()
            
            stock_data = {
                "id_product": novo_produto.id,
                "user_id": novo_produto.user_id,
                "category_id": novo_produto.category_id,
                "product_name": novo_produto.name,
                "product_price": float(novo_produto.price),
                "product_quantity": novo_produto.quantity,
                # "product_width": novo_produto.width,
                # "product_height": novo_produto.height,
                # "product_weight": novo_produto.weight,
                # "product_length": novo_produto.length,
                "variations": None,
            }
            Stock.create(stock_data)

            seo_data = {
                "product_id": novo_produto.id,
                "meta_title": request.form.get("meta_title", ""),
                "meta_description": request.form.get("meta_description", ""),
                "slug": request.form.get("slug", ProductController.formatar_nome(name)),
                "keywords": request.form.get("keywords", "")
            }

            ProductSeoController.create_product_seo(seo_data)

            return jsonify({"mensagem": "Produto adicionado com sucesso!", "product": novo_produto.to_dict()}), 201
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

        name = request.form.get("name", product.name)
        description = request.form.get("description", product.description)
        price = request.form.get("price", product.price)
        category_id = request.form.get("category_id", product.category_id)
        subcategory_id = request.form.get("subcategory_id", product.subcategory_id)
        quantity = request.form.get("quantity", product.quantity)
        width = request.form.get('width', product.width)
        height = request.form.get('height', product.height)
        weight = request.form.get('weight', product.weight)
        imagem = request.files.get("imagem")
        length = request.form.get('length', product.length)
        imagem_path = ProductController.upload_imagem(imagem, name) if imagem else product.image_path

        
        # Campos de SEO
        meta_title = request.form.get("meta_title")
        meta_description = request.form.get("meta_description")
        slug = request.form.get("slug")
        keywords = request.form.get("keywords")

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
            image_path=imagem_path
        )

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
                "variations": None,
            }

            stock_id = Stock.get_stock_id_by_product(product.id)
            if stock_id:
                Stock.update(stock_id, stock_data)

            #update SEO if provided
            if any([meta_title, meta_description, slug, keywords]):
                request.form = request.form.copy()  # Ensure request.form is mutable

                seo_data = {
                    "meta_title": request.form.get("meta_title"),
                    "meta_description": request.form.get("meta_description"),
                    "slug": request.form.get("slug"),
                    "keywords": request.form.get("keywords")
                }
                ProductSeoController.update_product_seo(product.id, seo_data)

            return jsonify({"mensagem": "Produto atualizado com sucesso!", "product": product.to_dict()}), 200
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
                Stock.delete_by_productId(product.id)
            except Exception as e:
                print(f'Erro ao excliur do estoque: {str(e)}')    
            
            product.delete()
            return jsonify({"mensagem": "Produto excluído com sucesso"}), 200
        except Exception as e:
            return jsonify({"erro": f"Erro ao excluir produto: {str(e)}"}), 500