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
def create_connection():
    return sqlite3.connect("database.db")

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
    print("Dados recebidos no registro:", data)  # Log para depuração

    # Extração dos dados
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')          # Nome completo (para tabela users)
    birth_date = data.get('birthDate')  # Data de nascimento (para tabela users)
    username = data.get('username')  # Nome de usuário único (para tabela profiles)
    avatar_url = data.get('avatarUrl', '')  # Opcional

    # Validação dos campos obrigatórios
    required_fields = {
        'email': email,
        'password': password,
        'name': name,
        'birthDate': birth_date,
        'username': username
    }
    
    missing_fields = [field for field, value in required_fields.items() if not value]
    if missing_fields:
        return jsonify({
            "error": "Campos obrigatórios faltando",
            "missing_fields": missing_fields
        }), 400

    # Verificar se o e-mail ou o nome de usuário já existem
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({"error": "E-mail já está em uso"}), 400
    
    cursor.execute('SELECT id FROM profiles WHERE username = ?', (username,))
    existing_username = cursor.fetchone()
    if existing_username:
        return jsonify({"error": "Nome de usuário já existe"}), 400

    # Criptografia da senha
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    try:
        cursor.execute('BEGIN TRANSACTION')
        
        # 1. Insere na tabela users (com name e birth_date)
        cursor.execute(
            'INSERT INTO users (email, password, name, birth_date) VALUES (?, ?, ?, ?)',
            (email, hashed_password, name, birth_date)
        )
        user_id = cursor.lastrowid
        
        # 2. Insere na tabela profiles
        cursor.execute(
            '''INSERT INTO profiles 
               (user_id, username, full_name, birth_date, avatar_url) 
               VALUES (?, ?, ?, ?, ?)''',
            (user_id, username, name, birth_date, avatar_url)
        )
        
        conn.commit()
        
        # Gera token JWT - Certifique-se de que o user_id seja uma string
        access_token = create_access_token(identity=str(user_id))  # Converte user_id para string
        
        return jsonify({
            "message": "Registro concluído com sucesso",
            "access_token": access_token,
            "user_id": user_id,
            "username": username
        }), 201
        
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if 'email' in str(e):
            return jsonify({"error": "E-mail já está em uso"}), 400
        elif 'username' in str(e):
            return jsonify({"error": "Nome de usuário já existe"}), 400
        return jsonify({"error": f"Erro de banco de dados: {str(e)}"}), 400
        
    except Exception as e:
        conn.rollback()
        print("Erro durante o registro:", str(e))
        return jsonify({"error": "Erro interno no servidor"}), 500
        
    finally:
        conn.close()
        
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
        profile = UserProfile.get_by_user_id(user_id)
        
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
    avatar_url = f'https://rua11storecatalogapi-production.up.railway.app/auth/{file_path}' #public url

    #update on database
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE profiles SET avatar_url = ? WHERE user_id = ?", (avatar_url, user_id))



    conn.commit()
    conn.close()

    return jsonify({"avatar_url": avatar_url}), 200

@auth_bp.route('/uploads/avatars/<filename>')
def uploaded_file(filename):
    print(filename)
    return send_from_directory(os.path.join(os.getcwd(), 'uploads', 'avatars'), filename)


# Rota de login
@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "E-mail e senha são obrigatórios"}), 400
    
    conn = create_connection()
    cursor = conn.cursor()

    # Buscar o usuário no banco de dados
    cursor.execute('SELECT id, name, email, password FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()

    if user is None:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    # Verificar se a senha está correta
    if not bcrypt.check_password_hash(user[3], password):
        return jsonify({"error": "Senha incorreta"}), 401
    
    # Gerar o token JWT - Certifique-se de que o user_id seja uma string
    token = create_access_token(identity=str(user[0]))  # Converte user_id para string

    return jsonify({"message": "Login realizado com sucesso!", "token": token}), 200

# Rota de logout
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # Obtém os dados do token JWT
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()
        
        print(f"Revogando token {jti} para usuário {user_id}")  # Debug
        
        # Adiciona à blocklist no banco de dados
        conn = create_connection()
        cursor = conn.cursor()
        
        # Verifica se a tabela existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS token_blocklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jti TEXT NOT NULL UNIQUE,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insere o token revogado
        cursor.execute(
            "INSERT INTO token_blocklist (jti, user_id) VALUES (?, ?)",
            (jti, user_id)
        )
        conn.commit()
        conn.close()
        
        return jsonify({"msg": "Logout realizado com sucesso"}), 200
        
    except sqlite3.IntegrityError:
        return jsonify({"error": "Token já revogado"}), 400
    except Exception as e:
        print(f"Erro no logout: {str(e)}")
        return jsonify({"error": "Falha no logout"}), 500
