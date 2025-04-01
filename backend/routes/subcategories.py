from flask import Blueprint
from controllers.sub_category_controller import SubCategoryController

# Cria um Blueprint para subcategorias
subcategory_bp = Blueprint('subcategory', __name__, url_prefix='/api/subcategories')

@subcategory_bp.route('/', methods=['POST'])
def create():
    """Cria uma nova subcategoria"""
    return SubCategoryController.create_subcategory()

@subcategory_bp.route('/<int:subcategory_id>', methods=['PUT'])
def update(subcategory_id):
    """Atualiza uma subcategoria existente"""
    return SubCategoryController.update_subcategory(subcategory_id)

@subcategory_bp.route('/<int:subcategory_id>', methods=['DELETE'])
def delete(subcategory_id):
    """Remove uma subcategoria"""
    return SubCategoryController.delete_subcategory(subcategory_id)

@subcategory_bp.route('/', methods=['GET'])
def get_all():
    """Lista todas as subcategorias"""
    return SubCategoryController.get_all_subcategories()

@subcategory_bp.route('/<int:subcategory_id>', methods=['GET'])
def get_one(subcategory_id):
    """Obtém uma subcategoria específica"""
    return SubCategoryController.get_subcategory_by_id(subcategory_id)

# Rota adicional para listar subcategorias de uma categoria específica
@subcategory_bp.route('/by_category/<int:category_id>', methods=['GET'])
def get_by_category(category_id):
    """Lista todas as subcategorias de uma categoria específica"""
    # Você precisaria implementar este método no controller
    return SubCategoryController.get_subcategories_by_category(category_id)