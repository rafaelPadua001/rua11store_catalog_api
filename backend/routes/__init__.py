from flask import Blueprint
from routes.authentication import auth_bp
from routes.categories import category_bp
from routes.products import products_bp
from routes.stock import stock_bp
from routes.melhorEnvio import melhorenvio_bp
from routes.mercadoPago import mercadoPago_bp
from routes.payments import payment_bp
from routes.delivery import delivery_bp
from routes.orders import orders_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(stock_bp, url_prefix='/stock')
    app.register_blueprint(melhorenvio_bp, url_prefix='/melhorEnvio')
    app.register_blueprint(mercadoPago_bp, url_prefix='/payment')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(delivery_bp, url_prefix='/delivery')
    app.register_blueprint(orders_bp, url_prefix='/order')