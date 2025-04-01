from flask import Blueprint
from routes.produtos import produtos_bp
from routes.authentication import auth_bp
from routes.categories import category_bp
from routes.subcategories import subcategory_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(produtos_bp)
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(subcategory_bp)
    
