from flask import Blueprint
from routes.produtos import produtos_bp
from routes.authentication import auth_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(produtos_bp)
    
