from flask import Blueprint, request, jsonify
from controllers.categoryController import CategoryController
from flask_cors import CORS

# Criação do Blueprint
category_bp = Blueprint('category', __name__)

# Configuração Global do CORS para esse Blueprint
CORS(category_bp, 
     resources={
         r"/*": {
             "origins": [
                 "https://rua11store-catalog-api.vercel.app",
                 "http://localhost:3000"
             ],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }
     })

@category_bp.route('/', methods=['GET', 'POST'])
def handle_categories():
    if request.method == 'GET':
        """Lista todas as categorias"""
        try:
            return CategoryController.get_all_categories()
        except Exception as e:
            print(f"Erro ao listar categorias: {str(e)}")
            return jsonify({"error": "Erro ao obter categorias"}), 500
        
    elif request.method == 'POST':
        """Cria uma nova categoria ou subcategoria"""
        try:
            if not request.is_json:
                return jsonify({"error": "Content-Type deve ser application/json"}), 415
            
            data = request.get_json(silent=True)
            if data is None:
                return jsonify({"error": "JSON inválido"}), 400
            
            # Corrigido: Passando a chamada corretamente, sem passar `data`
            return CategoryController.create_category()
        except Exception as e:
            print(f"Erro ao criar categoria: {str(e)}")
            return jsonify({"error": "Erro interno no processamento"}), 500

        


@category_bp.route('/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_category(category_id):
    if request.method == 'GET':
        """Obtém uma categoria específica"""
        try:
            return CategoryController.get_category_by_id(category_id)
        except Exception as e:
            print(f"Erro ao buscar categoria {category_id}: {str(e)}")
            return jsonify({"error": "Erro ao obter categoria"}), 500
        
    elif request.method == 'PUT':
        """Atualiza uma categoria existente"""
        try:
            if not request.is_json:
                return jsonify({"error": "Content-Type deve ser application/json"}), 415
            
            data = request.get_json(silent=True)
            if data is None:
                return jsonify({"error": "JSON inválido"}), 400
            
            return CategoryController.update_category(category_id, data)
        except Exception as e:
            print(f"Erro ao atualizar categoria {category_id}: {str(e)}")
            return jsonify({"error": "Erro interno ao atualizar categoria"}), 500

    elif request.method == 'DELETE':
        """Remove uma categoria"""
        try:
            return CategoryController.delete_category(category_id)
        except Exception as e:
            print(f"Erro ao deletar categoria {category_id}: {str(e)}")
            return jsonify({"error": "Erro ao deletar categoria"}), 500

# Middleware para garantir o CORS em todas as respostas
@category_bp.after_request
def after_request(response):
    allowed_origins = [
        "https://rua11store-catalog-api.vercel.app",
        "http://localhost:3000"
    ]
    origin = request.headers.get('Origin')
    
    if origin and origin in allowed_origins:
        response.headers.add('Access-Control-Allow-Origin', origin)

    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    return response
