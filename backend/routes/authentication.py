from flask import Blueprint, request, jsonify, current_app
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, get_jwt
import sqlite3
import datetime
from models.userProfile import UserProfile
import sys
from pathlib import Path
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from models.user import User
from models.userProfile import UserProfile, get_user_profile_by_user_id
from models.tokenBlockList import TokenBlocklist
from database import db


# Criando o Blueprint para autenticação
# Adiciona o diretório pai ao caminho de importação
sys.path.append(str(Path(__file__).parent.parent))

# Agora importe o UserProfile
from models.userProfile import UserProfile

auth_bp = Blueprint("auth", __name__)

bcrypt = Bcrypt()
CORS(
    auth_bp,
    resources={
        r"/*": {
            "origins": "*",
            "allow_headers": ["Authorization", "Content-Type"],
            "methods": ["GET", "POST", "OPTIONS"],  # Adicione OPTIONS se necessário
        }
    },
)

# Configuração do JWTManager
jwt = JWTManager()



# Função para criar a conexão com o banco de dados
def create_connection(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# Função para verificar se o token está na blocklist
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    conn = create_connection()
    cursor = conn.cursor()
    
    # Verifica se o token está na blocklist
    cursor.execute("SELECT jti FROM token_blocklist WHERE jti = ?", (jti,))
    result = cursor.fetchone()
    conn.close()
    
    return result is not None  # Retorna True se o token estiver revogado

# Rota de registro de usuário
@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    birth_date = data.get('birthDate')
    avatar_url = data.get('avatarUrl', '')

    if not all([email, password, name, birth_date]):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    # Verifica se usuário existe
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "E-mail já está em uso"}), 400

    if UserProfile.query.filter_by(username=name).first():
        return jsonify({"error": "Nome de usuário já existe"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    user = User(email=email, password=hashed_password, name=name, birth_date=birth_date)
    db.session.add(user)
    db.session.commit()

    profile = UserProfile(user_id=user.id, username=name, full_name=name, birth_date=birth_date, avatar_url=avatar_url)
    db.session.add(profile)
    db.session.commit()

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": "Registro concluído com sucesso",
        "access_token": access_token,
        "user_id": user.id,
        "username": name
    }), 201

        
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        # 1. Obter e validar o user_id do token
        user_id = get_jwt_identity()
        print(f"[DEBUG] Token user_id: {user_id} (type: {type(user_id)})")  # Log para diagnóstico
        
        if not user_id:
            return jsonify({"error": "Token inválido - ID de usuário ausente"}), 401

        # 2. Converter para inteiro se necessário
        try:
            user_id = int(user_id)
        except (TypeError, ValueError) as e:
            print(f"[ERROR] Falha ao converter user_id: {e}")
            return jsonify({
                "error": "Formato de ID inválido",
                "details": f"O ID deve ser numérico (recebido: {user_id})"
            }), 400

        # 3. Validar o ID
        if user_id <= 0:
            return jsonify({"error": "ID de usuário deve ser positivo"}), 400

        # 4. Buscar o perfil
        print(f"[DEBUG] Buscando perfil para user_id: {user_id}")
        profile = UserProfile.get_user_profile_by_user_id(user_id)
        
        if not profile:
            return jsonify({
                "error": "Perfil não encontrado",
                "user_id": user_id
            }), 404

        # 5. Montar resposta
        response_data = {
            "user_id": user_id,
            "username": profile.username,
            "full_name": profile.full_name,
            "birth_date": profile.birth_date,
            "avatar_url": profile.avatar_url or "" , # Garante string vazia se None
            "name": profile.name,
            "email": profile.email 
        }
        
        print(f"[DEBUG] Perfil encontrado: {response_data}")
        return jsonify(response_data), 200
        
    except sqlite3.Error as e:
        print(f"[DATABASE ERROR] Erro ao acessar banco de dados: {str(e)}")
        return jsonify({
            "error": "Erro no banco de dados",
            "details": str(e)
        }), 500
        
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {type(e).__name__}: {str(e)}")
        return jsonify({
            "error": "Erro interno no servidor",
            "details": f"{type(e).__name__}: {str(e)}"
        }), 500

@auth_bp.route('/upload-avatar', methods=["POST"])
@jwt_required()
def upload_avatar():
    #get file
    file = request.files.get('avatar')
    if not file:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    #save file
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads/avatars', filename)
    file.save(file_path)

    #update url avatar on database
    user_id = get_jwt_identity()
    avatar_url = f'https://rua11store-catalog-api-lbp7.onrender.com/{file_path}' #public url

    #update on database
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE profiles SET avatar_url = ? WHERE user_id = ?", (avatar_url, user_id))



    conn.commit()
    conn.close()

    return jsonify({"avatar_url": avatar_url}), 200

@auth_bp.route('/uploads/avatars/<filename>')
@jwt_required()
def uploaded_file(filename):
    print(filename)
    return send_from_directory('uploads/avatars', filename)


@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "E-mail e senha são obrigatórios"}), 400

    # Buscar o usuário usando SQLAlchemy ORM
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Verificar a senha
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Senha incorreta"}), 401

    # Criar o token JWT
    token = create_access_token(identity=str(user.id))

    return jsonify({"message": "Login realizado com sucesso!", "token": token}), 200


# Rota de logout
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()
        
        print(f"Revogando token {jti} para usuário {user_id}")
        
        # Verifica se o token já está na blocklist para evitar duplicidade
        existing = TokenBlocklist.query.filter_by(jti=jti).first()
        if existing:
            return jsonify({"msg": "Token já revogado"}), 400
        
        revoked_token = TokenBlocklist(jti=jti, user_id=user_id)
        db.session.add(revoked_token)
        db.session.commit()
        
        return jsonify({"msg": "Logout realizado com sucesso"}), 200

    except Exception as e:
        print(f"Erro ao revogar token: {str(e)}")
        return jsonify({"error": "Erro interno"}), 500
