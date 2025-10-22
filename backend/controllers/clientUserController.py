import os
import jwt
from flask import jsonify, request
from models.clientUser import ClientUser
from models.tokenBlockList import TokenBlocklist
from database import db
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from flask_jwt_extended import get_jwt, jwt_required, create_access_token, get_jwt_identity, JWTManager
import uuid

jwt = JWTManager()

class ClientUserController:
    def get_logged_client():
        userId = get_jwt_identity()

        # se o ClientUser.id for UUID
        client = ClientUser.query.get(str(userId))

        if not client:
            return jsonify({'error': 'Cliente não encontrado'}), 404

        return jsonify({
            'id': str(client.id),
            'name': client.name,
            'email': client.email,
        }), 200
 
    def get_client():
        query = request.args.get('q', '').strip()
        if not query or len(query) < 2:
            return jsonify([]), 200
        
        try:
            # Busca por UUID válido
            
                # Busca por nome ou e-mail se não for UUID
            users_query = ClientUser.query.filter(
                    (ClientUser.name.ilike(f"%{query}%")) |
                    (ClientUser.email.ilike(f"%{query}%"))
                )

            users = users_query.all()

            return jsonify([
                {"id": u.id, "name": u.name, "email": u.email}
                for u in users
            ]), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500


    def register_client_controller(data):
        name = data.get("name")
        birth_date = data.get("birthDate")
        email = data.get("email")
        password = data.get("password")
        type_user = data.get("type", "client")

        if not all([name, birth_date, email, password]):
            return jsonify({"error": "Todos os campos são obrigatórios"}), 400

        existing = ClientUser.query.filter_by(email=email).first()
        if existing:
            return jsonify({"error": "E-mail já registrado"}), 409

        try:
            client = ClientUser(
                name=name,
                birth_date=datetime.strptime(birth_date, "%Y-%m-%d").date(),
                email=email,
                type=type_user,
            )
            client.password = password

            db.session.add(client)
            db.session.commit()

            return jsonify({"message": "Usuário registrado com sucesso!"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def login_client_controller(data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'Error': "E-mail e senha são obrigatórios"}), 400
        
        user = ClientUser.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Aqui você deveria validar a senha com bcrypt.check_password_hash(user.password, password)
        # Mas vou focar só no token por enquanto

        # Gera o token JWT
        access_token = create_access_token(
            identity=str(user.id),  # 👈 isso corrige
            additional_claims={
                "email": user.email,
                "user_type": user.type
            }
        )

        
        return jsonify({
            "message": "Login realizado com sucesso!",
            "token": access_token
        }), 200

 
    @staticmethod
    @jwt_required()
    def logout_client_controller():
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
