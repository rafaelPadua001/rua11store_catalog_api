from flask import request, jsonify
from models.sub_category import SubCategory
from models.category import Category

class SubCategoryController:
    @staticmethod
    def create_subcategory():
        data = request.json
        name = data.get('name')
        category_id = data.get('category_id')

        if not name or not category_id:
            return jsonify({"error": "Name and category_id are required"}), 400
        
        category = Category.get_by_id(category_id)

        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        subcategory = SubCategory(name=name, category_id=category_id)
        subcategory.save()

        return jsonify({"message": "Subcategory created successfully", "id": subcategory.id}), 201

    @staticmethod
    def update_subcategory(subcategory_id):
        data = request.json
        subcategory = SubCategory.get_by_id(subcategory_id)

        if not subcategory:
            return jsonify({"error": "Subcategory not found"}), 404
        
        subcategory_instance = SubCategory(id=subcategory_id, 
                                           name=data.get("name", subcategory["name"]),
                                           category_id=data.get("category_id", subcategory["category_id"]))
        subcategory_instance.save()

        return jsonify({"message": "Subcategory updated successfully"}), 200
    
    @staticmethod
    def delete_subcategory(subcategory_id):
        subcategory = SubCategory.get_by_id(subcategory_id)

        if not subcategory:
             return jsonify({"error": "Subcategory not found"}), 404

        subcategory_instance = SubCategory(id=subcategory_id)
        subcategory_instance.delete()

    @staticmethod
    def get_all_subcategories():
        subcategories = SubCategory.get_all()
        return jsonify(subcategories), 200
    
    @staticmethod
    def get_subcategory_by_id(subcategory_id):
        subcategory = SubCategory.get_by_id(subcategory_id)

        if subcategory:
            return jsonify(subcategory), 200
        return jsonify({"error": "Subcategory not found"}), 404
    
    @staticmethod
    def get_subcategories_by_category(category_id):
        category = Category.get_by_id(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        subcategories = SubCategory.get_by_category(category_id)
        return jsonify(subcategories), 200