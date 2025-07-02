from flask import Blueprint
from routes.authentication import auth_bp
from routes.pages import pages_bp
from routes.categories import category_bp
from routes.products import products_bp
from routes.productsSeo import product_seo_bp
from routes.stock import stock_bp
from routes.melhorEnvio import melhorenvio_bp
from routes.mercadoPago import mercadoPago_bp
from routes.payments import payment_bp
from routes.delivery import delivery_bp
from routes.orders import orders_bp
from routes.webhook import webhook_bp
from routes.email import email_bp
from routes.seo import seo_bp
from routes.notification import notification_bp
from routes.coupon import coupon_bp
from routes.sitemap import sitemap_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(pages_bp, url_prefix='/pages')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(product_seo_bp, url_prefix='/product-seo')
    app.register_blueprint(stock_bp, url_prefix='/stock')
    app.register_blueprint(melhorenvio_bp, url_prefix='/melhorEnvio')
    app.register_blueprint(mercadoPago_bp, url_prefix='/payment')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(delivery_bp, url_prefix='/delivery')
    app.register_blueprint(orders_bp, url_prefix='/order')
    app.register_blueprint(webhook_bp, url_prefix='/webhook')
    app.register_blueprint(email_bp, url_prefix='/email')
    app.register_blueprint(seo_bp, url_prefix='/seo')
    app.register_blueprint(notification_bp, url_prefix='/notifications')
    app.register_blueprint(coupon_bp, url_prefix='/coupon')
    app.register_blueprint(sitemap_bp, url_prefix='/sitemap')