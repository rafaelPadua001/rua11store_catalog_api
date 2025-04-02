import os
from flask import jsonify, request
from werkzeug.utils import secure_filename
from database import db
from models.product import Product
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request


UPLOAD_FOLDER = "uploads/product_images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def formatar_nome(nome):
    """Remove espaços e caracteres especiais do nome do produto."""
    return secure_filename(nome.replace(" ", "_"))

def upload_imagem(imagem, product_name):
    """Salva a imagem na pasta 'uploads/product_images/NOME_DO_PRODUTO/' e retorna o caminho."""
    if imagem and allowed_file(imagem.filename):
        filename = secure_filename(imagem.filename)
        product_folder = os.path.join(UPLOAD_FOLDER, product_name)
        os.makedirs(product_folder, exist_ok=True)  # Cria a pasta do produto se não existir
        filepath = os.path.join(product_folder, filename)
        imagem.save(filepath)
        return filepath  # Retorna o caminho completo da imagem
    return None

def listar_produtos():
    """Retorna todos os produtos em formato JSON."""
    products = Product.get_all()
    return jsonify([p.to_dict() for p in products])  # Certifique-se de que Product tem um método to_dict()

def adicionar_produto():
    """Adiciona um novo produto ao banco de dados."""
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    category_id = request.form.get("category_id")
    subcategory_id = request.form.get("subcategory_id")
    quantity = request.form.get("quantity", 1)

   
    imagem = request.files.get("imagem")
    product_name = formatar_nome(name) if name else "produto_sem_nome"
    imagem_path = upload_imagem(imagem, product_name) if imagem else None

    print("Verificando JWT...")
    verify_jwt_in_request()  # Isso garante que o JWT seja verificado antes de acessar o conteúdo
    user_id = get_jwt_identity()
    print(f"Usuário autenticado: {user_id}")
    if not user_id:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    try:
        novo_produto = Product(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            subcategory_id=subcategory_id,
            image_path=imagem_path,  # Salva apenas o caminho da imagem
            quantity=quantity,
            user_id=user_id
        )
        novo_produto.save()
        
        return jsonify({
            "mensagem": "Produto adicionado com sucesso!",
            "product": {
                "id": novo_produto.id,
                "name": novo_produto.name,
                "description": novo_produto.description,
                "price": novo_produto.price,
                "category_id": novo_produto.category_id,
                "subcategory_id": novo_produto.subcategory_id,
                "quantity": novo_produto.quantity,
                "image": novo_produto.image_path  # Certifique-se de que a imagem está no retorno
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao adicionar produto: {str(e)}"}), 500

def update_product_data(product_id):
    """Atualiza os dados de um produto existente e retorna os dados atualizados."""
    verify_jwt_in_request()  # Garante que o usuário está autenticado
    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({"erro": "Usuário não autenticado"}), 401

    conn = Product.get_db_connection()
    cursor = conn.cursor()

    try:
        # Verifica se o produto existe e pertence ao usuário autenticado
        cursor.execute("SELECT id, image_path FROM products WHERE id = ? AND user_id = ?", 
                      (product_id, user_id))
        product = cursor.fetchone()

        if not product:
            return jsonify({"erro": "Produto não encontrado ou sem permissão para editar"}), 404

        existing_image_path = product[1]  # Caminho da imagem já salva

        # Obtém os dados do formulário
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        category_id = request.form.get("category_id")
        subcategory_id = request.form.get("subcategory_id")
        quantity = request.form.get("quantity")

        # Valida os valores
        price = float(price) if price and price.replace('.', '', 1).isdigit() else None
        quantity = int(quantity) if quantity and quantity.isdigit() else None

        # Processa a nova imagem (se enviada)
        imagem = request.files.get("imagem")
        imagem_path = upload_imagem(imagem, name) if imagem else existing_image_path  # Mantém a imagem antiga se nenhuma nova for enviada

        # Atualiza os dados no banco de dados
        cursor.execute("""
            UPDATE products 
            SET name = ?, description = ?, price = ?, category_id = ?, 
                subcategory_id = ?, quantity = ?, image_path = ?
            WHERE id = ? AND user_id = ?
        """, (name, description, price, category_id, subcategory_id, quantity, imagem_path, product_id, user_id))

        conn.commit()

        # Busca os dados atualizados do produto para retornar
        cursor.execute("""
            SELECT id, name, description, price, category_id, 
                   subcategory_id, quantity, image_path, user_id
            FROM products 
            WHERE id = ?
        """, (product_id,))
        
        updated_product = cursor.fetchone()
        
        if updated_product:
            # Converte para dicionário para retornar como JSON
            produto_atualizado = {
                "id": updated_product[0],
                "name": updated_product[1],
                "description": updated_product[2],
                "price": float(updated_product[3]) if updated_product[3] else None,
                "category_id": updated_product[4],
                "subcategory_id": updated_product[5],
                "quantity": updated_product[6],
                "image_path": updated_product[7],
                "user_id": updated_product[8]
            }
            
            return jsonify({
                "mensagem": "Produto atualizado com sucesso!",
                "product": produto_atualizado
            }), 200

        return jsonify({"erro": "Produto atualizado mas não foi possível recuperar os dados"}), 500

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Erro ao atualizar produto: {str(e)}"}), 500

    finally:
        conn.close()
