from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models.category import Category
from models.userProfile import UserProfile

def validate_category_data(data):
    """Função auxiliar para validar os dados da categoria."""
    if not data or not isinstance(data, dict):
        return "Dados inválidos"
    
    name = data.get('name')
    if not name or not isinstance(name, str) or not name.strip():
        return "Nome inválido"
    
    if data.get('is_subcategory', False) and not data.get('parent_id'):
        return "Categoria pai é obrigatória"
    
    return None

class CategoryController:
    
    @staticmethod
    def create_category():
        try:
            print("Verificando JWT...")
            verify_jwt_in_request()  # Isso garante que o JWT seja verificado antes de acessar o conteúdo
            current_user_id = get_jwt_identity()  # Esperando um ID do usuário

            print(f"Usuário autenticado: {current_user_id}")  # Verifique o que está sendo retornado

            if not current_user_id:
                return jsonify({"error": "Usuário não autenticado ou dados inválidos no JWT"}), 401

            # Buscar dados completos do usuário com a função correta
            current_user = UserProfile.get_by_user_id(current_user_id)
            if not current_user:
                return jsonify({"error": "Usuário não encontrado"}), 404

            data = request.get_json()
            
            error = validate_category_data(data)
            if error:
                return jsonify({"error": error}), 400

            name = data['name'].strip()
            is_subcategory = data.get('is_subcategory', False)
            parent_id = data.get('parent_id') if is_subcategory else None

            if parent_id:
                parent = Category.get_by_id(parent_id)
                if not parent:
                    return jsonify({"error": "Categoria pai não encontrada"}), 404
                if parent.is_subcategory:
                    return jsonify({"error": "Hierarquia inválida"}), 400
            
            category = Category(
                name=name,
                is_subcategory=is_subcategory,
                parent_id=parent_id,
                user_id=current_user.user_id  # Usando o user_id corretamente
            )
            
            if not category.save():
                return jsonify({"error": "Erro ao salvar categoria"}), 500

            return jsonify({
                "success": True,
                "category": {
                    "id": category.id,
                    "name": category.name,
                    "is_subcategory": category.is_subcategory,
                    "parent_id": category.parent_id
                }
            }), 201

        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            return jsonify({"error": "Erro interno"}), 500

    # @staticmethod
    def update_category(self,category_id):
        try:
            data = request.get_json()
            
            # Verificar se category_id é um dicionário e acessar a chave 'id'
            if isinstance(category_id, dict):
                category_id = category_id['id']  # Acessa o id do dicionário
            
            print(f"Buscando categoria com ID: {category_id}")

            category = Category.get_by_id(category_id)

            if not category:
                return jsonify({"error": "Categoria não encontrada"}), 404
            
            # Verificar se há alterações no nome
            if 'name' in data:
                category.name = data['name'].strip()
            
            # Verificar se há alterações no tipo de subcategoria
            if 'is_subcategory' in data:
                category.is_subcategory = bool(data['is_subcategory'])
            
            # Verificar se há alterações no ID da categoria pai
            if 'parent_id' in data:
                parent_id = data['parent_id'] if category.is_subcategory else None
                if parent_id:
                    parent = Category.get_by_id(parent_id)
                    if not parent:
                        return jsonify({"error": "Categoria pai não encontrada"}), 404
                    if parent.is_subcategory:
                        return jsonify({"error": "Não é possível criar subcategoria de outra subcategoria"}), 400
                category.parent_id = parent_id
            
            # Tentar salvar as alterações
            if not category.save():
                return jsonify({"error": "Falha ao atualizar categoria"}), 500

            return jsonify({
                "success": True,
                "message": "Categoria atualizada com sucesso",
                "category": {
                    "id": category.id,
                    "name": category.name,
                    "is_subcategory": category.is_subcategory,
                    "parent_id": category.parent_id
                }
            }), 200
        except Exception as e:
            print(f"Erro ao atualizar categoria: {str(e)}")
            return jsonify({"error": "Erro interno no servidor"}), 500

        
    @staticmethod
    def delete_category(category_id):
        try:
            category = Category.get_by_id(category_id)
            if not category:
                return jsonify({"error": "Categoria não encontrada"}), 404
            
            # Deletar a categoria
            if not category.delete():
                return jsonify({"error": "Erro ao excluir categoria"}), 500
            
            return jsonify({"message": "Categoria excluída com sucesso"}), 200
        except Exception as e:
            print(f"Erro ao excluir categoria: {str(e)}")
            return jsonify({"error": "Erro interno no servidor"}), 500
    
    @staticmethod
    def get_all():
        """Retorna todas as categorias do banco de dados"""
        try:
            categories = Category.get_all()  # Chamando o método estático get_all da Categoria
            return jsonify([category.to_dict() for category in categories]), 200  # Convertendo as categorias para dicionário e retornando como JSON
        except sqlite3.Error as e:
            print(f"Erro ao buscar categorias: {str(e)}")
            return jsonify({"error": "Erro ao buscar categorias"}), 500
    
    @staticmethod
    def get_all_categories():
        try:
            categories = Category.get_all()  # Método que retorna todas as categorias
            return jsonify([category.to_dict() for category in categories])
        except Exception as e:
            print(f"Erro ao listar categorias: {str(e)}")
            return jsonify({"error": "Erro ao listar categorias"}), 500

    @staticmethod
    def get_category_by_id(category_id):
        try:
            category = Category.get_by_id(category_id)
            if category:
                return jsonify(category.to_dict()), 200  # Convertendo para dicionário e retornando como JSON
            return jsonify({"error": "Categoria não encontrada"}), 404
        except Exception as e:
            print(f"Erro ao buscar categoria: {str(e)}")
            return jsonify({"error": "Erro interno no servidor"}), 500
