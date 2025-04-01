from flask import request, jsonify
from models.category import Category
from datetime import datetime

class CategoryController:
  
    @staticmethod
    def create_category():
        try:
            data = request.get_json()
            
            # Validação básica
            if not data or not isinstance(data, dict):
                return jsonify({"error": "Dados inválidos"}), 400

            name = data.get('name')
            is_subcategory = data.get('is_subcategory', False)
            parent_id = data.get('parent_id')

            # Validação do nome
            if not name or not isinstance(name, str) or not name.strip():
                return jsonify({"error": "Nome inválido"}), 400

            # Validação para subcategorias
            if is_subcategory:
                if not parent_id:
                    return jsonify({"error": "Categoria pai é obrigatória"}), 400
                
                parent = Category.get_by_id(parent_id)
                if not parent:
                    return jsonify({"error": "Categoria pai não encontrada"}), 404
                
                if parent.is_subcategory:
                    return jsonify({"error": "Hierarquia inválida"}), 400

            # Cria e salva a categoria
            category = Category(
                name=name.strip(),
                is_subcategory=is_subcategory,
                parent_id=parent_id if is_subcategory else None
            )
            
            # Salvamento com tratamento de erro
            try:
                category.save()  # Agora o save() retorna True/False
            except Exception as e:
                print(f"Erro ao salvar no banco: {str(e)}")
                return jsonify({"error": "Erro ao salvar categoria"}), 500

            # Resposta de sucesso
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

    @staticmethod
    def update_category(category_id):
        try:
            data = request.get_json()
            
            # Obter a categoria existente
            category = Category.get_by_id(category_id)
            if not category:
                return jsonify({"error": "Categoria não encontrada"}), 404
            
            # Atualizar apenas os campos fornecidos
            if 'name' in data:
                category.name = data['name'].strip()
            
            if 'is_subcategory' in data:
                category.is_subcategory = bool(data['is_subcategory'])
            
            if 'parent_id' in data:
                # Validação adicional para subcategorias
                if category.is_subcategory and not data['parent_id']:
                    return jsonify({"error": "Categoria pai é obrigatória para subcategorias"}), 400
                
                if data['parent_id']:
                    parent = Category.get_by_id(data['parent_id'])
                    if not parent:
                        return jsonify({"error": "Categoria pai não encontrada"}), 404
                    if parent.is_subcategory:
                        return jsonify({"error": "Não é possível criar subcategoria de outra subcategoria"}), 400
                
                category.parent_id = data['parent_id'] if category.is_subcategory else None

            # Salvar as alterações
            try:
                if not category.save():
                    return jsonify({"error": "Falha ao atualizar categoria"}), 500
            except Exception as e:
                print(f"Erro ao salvar categoria: {str(e)}")
                return jsonify({"error": "Erro no banco de dados"}), 500

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
        category = Category.get_by_id(category_id)

        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        category_instance = Category(id=category_id)
        category_instance.delete()

        return jsonify({"message": "Category deleted successfully"}), 200
    
    @staticmethod
    def get_all_categories():
        categories = Category.get_all()
        return jsonify(categories), 200

    @staticmethod
    def get_category_by_id(category_id):
        category = Category.get_by_id(category_id)
        if category:
            return jsonify(category), 200
        return jsonify({"error": "Category not found"}), 404