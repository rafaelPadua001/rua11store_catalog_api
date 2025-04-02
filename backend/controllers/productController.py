import os
from flask import jsonify, request
from werkzeug.utils import secure_filename
from database import db
from models.product import Product

UPLOAD_FOLDER = "uploads/product_images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

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

def adicionar_produto(data):
    """Adiciona um novo produto ao banco de dados."""
    imagem = request.files.get("imagem")  # Obtém a imagem enviada no formulário
    product_name = formatar_nome(data.get("name", ""))  # Formata o nome para criar a pasta
    imagem_path = upload_imagem(imagem, product_name) if imagem else None

    user_id = data.get("user_id")  # Obtém o user_id da requisição

    if not user_id:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    try:
        novo_produto = Product(
            nome=data["name"],
            descricao=data["description"],
            preco=data["price"],
            categoria_id=data.get("category_id"),
            subcategoria_id=data.get("subcategory_id"),
            imagem=imagem_path,  # Salva apenas o caminho da imagem
            quantidade=data.get("quantity", 1),
            user_id=user_id  # Agora pega corretamente do data
        )
        db.session.add(novo_produto)
        db.session.commit()
        
        return jsonify({
            "mensagem": "Produto adicionado com sucesso!",
            "imagem": imagem_path
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao adicionar produto: {str(e)}"}), 500
