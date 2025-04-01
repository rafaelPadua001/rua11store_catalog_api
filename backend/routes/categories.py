from flask import Blueprint, request, jsonify, make_response
from controllers.categoryController import CategoryController
from flask_cors import CORS

# Criação do Blueprint
category_bp = Blueprint('category', __name__)

# Configuração Global do CORS para esse Blueprint
CORS(category_bp, 
     origins="*",
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type"],
     expose_headers=["Content-Disposition"])

@category_bp.route('/', methods=['GET', 'POST'])
def handle_categories():
    if request.method == 'GET':
        """Lista todas as categorias"""
        return CategoryController.get_all_categories()
        
    elif request.method == 'POST':
        """Cria uma nova categoria ou subcategoria"""
        try:
            # Verifica se há dados JSON
            if not request.is_json:
                return jsonify({"error": "Content-Type deve ser application/json"}), 415
                
            return CategoryController.create_category()
            
        except Exception as e:
            print(f"Erro na rota: {str(e)}")
            return jsonify({"error": "Erro interno no processamento"}), 500
            
    elif request.method == 'OPTIONS':
        """Responde às requisições de preflight CORS"""
        response = jsonify()
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
        return response

@category_bp.route('/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_category(category_id):
    if request.method == 'GET':
        """Obtém uma categoria específica"""
        return CategoryController.get_category_by_id(category_id)
    elif request.method == 'PUT':
        """Atualiza uma categoria existente"""
        return CategoryController.update_category(category_id)
    elif request.method == 'DELETE':
        """Remove uma categoria"""
        return CategoryController.delete_category(category_id)

# Middleware para garantir o CORS em todas as respostas
@category_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response
