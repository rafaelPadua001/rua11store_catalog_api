from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import Config
from database import db
from routes import register_routes
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__, static_folder="uploads", static_url_path="/uploads")

app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}})
bcrypt = Bcrypt(app)

app.config["JWT_SECRET_KEY"] = "headers"
jwt = JWTManager(app)

# Inicializa o banco de dados
db.init_app(app)

# Registrar as rotas
register_routes(app)

# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
