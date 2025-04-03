from flask import Blueprint
from routes.authentication import auth_bp
from routes.categories import category_bp
# from routes.subcategories import subcategory_bp
from routes.products import products_bp
from routes.stock import stock_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(category_bp, url_prefix='/categories')
    # app.register_blueprint(subcategory_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(stock_bp, url_prefix='/stock')
