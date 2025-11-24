from flask import Blueprint, request, jsonify, current_app
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token, get_jwt
from itsdangerous import URLSafeTimedSerializer
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
from controllers.emailController import EmailController
from database import db


sys.path.append(str(Path(__file__).parent.parent))


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

serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY", "your-secret-key"))


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

    #new datas
    user_type = data.get('type', 'admin')
    #fcm_token = data.get('fcm_token')

    if not all([email, password, name, birth_date]):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    # Verifica se usuário existe
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "E-mail já está em uso"}), 400

    if UserProfile.query.filter_by(username=name).first():
        return jsonify({"error": "Nome de usuário já existe"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    user = User(email=email, password=hashed_password, name=name, birth_date=birth_date, type=user_type,
                 #fcm_token=fcm_token
                )
    db.session.add(user)
    db.session.commit()

    profile = UserProfile(user_id=user.id, username=name, full_name=name, birth_date=birth_date, avatar_url=avatar_url, phone='(00) 00000-0000', mobile='(00) 00000-0000')
    db.session.add(profile)
    db.session.commit()

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": "Registro concluído com sucesso",
        "access_token": access_token,
        "user_id": user.id,
        "username": name
    }), 201


@auth_bp.route('/user/<uuid:userId>', methods=['GET'])
@jwt_required()
def get_auth_user(userId):
    current_user_id = get_jwt_identity()

    if str(userId) != str(current_user_id):
        return jsonify({'error': 'Acesso não autorizado'}), 403

    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    return jsonify({
        'id': str(user.id),
        'name': user.name,
        'email': user.email,
        'avatar': user.avatar,
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        # 1. Obter e validar o user_id do token
        user_id = get_jwt_identity()
       # print(f"[DEBUG] Token user_id: {user_id} (type: {type(user_id)})")  # Log para diagnóstico
        
        if not user_id:
            return jsonify({"error": "Token inválido - ID de usuário ausente"}), 401

        # 2. Converter para inteiro se necessário
        try:
            user_id = int(user_id)
        except (TypeError, ValueError) as e:
           # print(f"[ERROR] Falha ao converter user_id: {e}")
            return jsonify({
                "error": "Formato de ID inválido",
                "details": f"O ID deve ser numérico (recebido: {user_id})"
            }), 400

        # 3. Validar o ID
        if user_id <= 0:
            return jsonify({"error": "ID de usuário deve ser positivo"}), 400

        # 4. Buscar o perfil
        #print(f"[DEBUG] Buscando perfil para user_id: {user_id}")
        profile = get_user_profile_by_user_id(db.session, user_id)
        
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
            # "name": profile.name,
            # "email": profile.email 
        }
        
       # print(f"[DEBUG] Perfil encontrado: {response_data}")
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
    refresh_token= create_refresh_token(identity=user.id)

    return jsonify({"message": "Login realizado com sucesso!", "access_token": token, "refresh_token": refresh_token}), 200

#rota refresh token 
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200

# Rota de logout
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()
        
        print(f"Revogando token {jti} para usuário {user_id}")
        
        # ⚡ DETECTAR automaticamente o tipo de ID
        if isinstance(user_id, int):
            # É um admin (integer)
            user_id_str = str(user_id)
            print(f"👤 Admin detectado (ID: {user_id_str})")
        else:
            # É um client (UUID ou string)
            user_id_str = str(user_id)
            print(f"👤 Client detectado (ID: {user_id_str})")
        
        # Verifica se o token já está na blocklist
        existing = TokenBlocklist.query.filter_by(jti=jti).first()
        if existing:
            return jsonify({"msg": "Token já revogado"}), 400
        
        # ⚡ Salva como string (funciona para ambos)
        revoked_token = TokenBlocklist(jti=jti, user_id=user_id_str)
        db.session.add(revoked_token)
        db.session.commit()
        
        return jsonify({"msg": "Logout realizado com sucesso"}), 200

    except Exception as e:
        print(f"Erro ao revogar token: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Erro interno"}), 500


@auth_bp.route('/recoveryPassword', methods=['POST'])
def recovery_password():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({"error": "E-mail é obrigatório"}), 400
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    token = serializer.dumps(email, salt="password-recovery")


    # (Opcional) Salvar o token no banco se quiser controle mais rígido
        # user.recovery_token = token
        # db.session.commit()

    recovery_link = f"https://rua11store-catalog-api.vercel.app/authenticator/resetPassword?token={token}"
    EmailController.send_email(
    "Recuperação de senha",
    [email], 
    f"Clique aqui para redefinir sua senha: {recovery_link}",
    f"<p>Clique <a href='{recovery_link}'>aqui</a> para redefinir sua senha.</p>"
)


    return jsonify({"message": "E-mail de recuperação enviado com sucesso"}), 200

@auth_bp.route('/resetPassword', methods=['POST'])
def reset_password():
    data = request.json
    token = data.get('token')
    new_password = data.get('newPassword')  # usa 'newPassword' camelCase

    if not token or not new_password:
        return jsonify({"error": "Token e nova senha são obrigatórios"}), 400

    try:
        email = serializer.loads(token, salt="password-recovery", max_age=3600)
    except Exception:
        return jsonify({"error": "Token inválido ou expirado"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
    user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Senha redefinida com sucesso"}), 200


