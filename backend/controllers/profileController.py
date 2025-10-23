import json
import uuid
from datetime import datetime
from flask import request, jsonify
from models.userProfile import UserProfile
from models.address import Address
from models.clientUser import ClientUser
from models.user import User
from models.cartItems import CartItems
from controllers.addressController import AddressController
from database import db
from sqlalchemy.orm import Session
from typing import Optional
import cloudinary.uploader

class ProfileController:
    @staticmethod
    def get_user_profile_by_user_id(session, userId):
        try:
            if not userId or userId.lower() == "null" or userId.lower() == "undefined":
                print("UserId inválido:", userId)
                return None
            # Detecta se é string que parece número inteiro
            if isinstance(userId, str) and userId.isdigit():
                filter_value = int(userId)
            else:
                filter_value = userId  # string UUID
            # Busca perfil
            profile = session.query(UserProfile).filter_by(user_id=filter_value).first()
            if not profile:
                return None
            # Busca endereços
            addresses = session.query(Address).filter_by(client_user_id=filter_value).all()
            address_list = []
            for addr in addresses:
                address_list.append({
                    "id": addr.id,
                    "street": addr.logradouro,
                    "number": addr.numero,
                    "complement": addr.complemento,
                    "neighborhood": addr.bairro,
                    "city": addr.cidade,
                    "state": addr.estado,
                    "zip": addr.cep,
                    "country": addr.pais,
                    "referencia": addr.referencia
                })
            # Retorna como dict
            return {
                "id": profile.id,
                "user_id": profile.user_id,
                "username": profile.username,
                "full_name": profile.full_name,
                "birth_date": profile.birth_date.isoformat()
                        if hasattr(profile.birth_date, "isoformat")
                        else profile.birth_date,
                "avatar_url": profile.avatar_url,
                "phone": profile.phone,
                "mobile": profile.mobile,
                "created_at": profile.created_at.strftime("%Y-%m-%dT%H:%M:%S") 
                    if isinstance(profile.created_at, datetime) 
                    else profile.created_at,
                "updated_at": profile.updated_at.strftime("%Y-%m-%dT%H:%M:%S") 
                    if isinstance(profile.updated_at, datetime) 
                    else profile.updated_at,
                "addresses": address_list
            }
              
        except Exception as e:
            print(f"Erro ao buscar perfil: {e}")
            raise

    @staticmethod
    def update_profile(userId):
        try:
            # Validação do userId
            if not userId or userId == 'null' or userId == 'undefined':
                return jsonify({"error": "UserId é obrigatório"}), 400
            
            # Usar userId como string
            user_id_str = str(userId)

            # Detecta se vem multipart/form-data ou JSON
            if request.content_type.startswith("multipart/form-data"):
                data = request.form.to_dict()
                avatar_file = request.files.get('avatar_file')
            else:
                data = request.get_json() or {}
                avatar_file = None

            # Busca perfil
            profile = UserProfile.query.filter_by(user_id=user_id_str).first()

            # Upload do avatar se existir
            avatar_url = None
            if avatar_file:
                avatar_url = ProfileController.upload_avatar_to_cloudinary(avatar_file)
              

            # Processa dados de endereço
            address_data = None
            addresses_field = data.get('addresses') or data.get('address')
            if addresses_field:
                if isinstance(addresses_field, str):
                    try:
                        address_data = json.loads(addresses_field)
                    except json.JSONDecodeError as e:
                        print(f"Erro ao decodificar JSON do endereço: {e}")
                        address_data = None
                elif isinstance(addresses_field, dict):
                    address_data = addresses_field


            # Atualiza ou cria perfil
            if profile:
                profile.full_name = data.get('full_name', profile.full_name or '')
                profile.username = data.get('username', data.get('user_name', profile.username or ''))
                profile.phone = data.get('phone', profile.phone or '')
                profile.mobile = data.get('mobile', profile.mobile or '')
                
                birth_date = data.get('birth_date')
                if birth_date:
                    profile.birth_date = birth_date

                if avatar_url:
                    profile.avatar_url = avatar_url
            else:
                profile = UserProfile(
                    user_id=user_id_str,
                    full_name=data.get('full_name', ''),
                    username=data.get('username', data.get('user_name', '')),
                    birth_date=data.get('birth_date'),
                    avatar_url=avatar_url or '',
                    phone=data.get('phone', ''),
                    mobile=data.get('mobile', '')
                )
                db.session.add(profile)

            # Processa endereço apenas se dados válidos
            address_info = {}
            if address_data:
                # Verifica se já existe endereço para este usuário
                existing_address = Address.query.filter_by(client_user_id=user_id_str).first()
                
                if existing_address:
                    # Atualiza endereço existente
                    address_result = AddressController.update_address(user_id_str, existing_address.id, address_data)
                else:
                    # Cria novo endereço
                    address_result = AddressController.create_address(user_id_str, address_data)

                if isinstance(address_result, dict):
                    # aceita tanto 'address' quanto 'addresses'
                    if 'address' in address_result:
                        address_info = address_result['address']
                    elif 'addresses' in address_result:
                        address_info = address_result['addresses']
                    elif 'error' in address_result:
                        print("Erro ao processar endereço:", address_result['error'])
                    else:
                        print("Estrutura inesperada de retorno do endereço:", address_result)
                else:
                    print("Resultado inesperado do endereço:", address_result)



            db.session.commit()

            # Formata a resposta de forma segura
            response_data = {
                "user_id": profile.user_id,
                "full_name": profile.full_name,
                "username": profile.username,
                "avatar_url": profile.avatar_url or "",
                "phone": profile.phone,
                "mobile": profile.mobile,
                "address": address_info
            }
            
            # Tratamento seguro da data
            if profile.birth_date:
                if hasattr(profile.birth_date, 'isoformat'):
                    response_data["birth_date"] = profile.birth_date.isoformat()
                else:
                    response_data["birth_date"] = str(profile.birth_date)
            else:
                response_data["birth_date"] = None

            return jsonify(response_data), 200

        except Exception as e:
            db.session.rollback()
            print(f"Error ao atualizar perfil: {e}")
            return jsonify({"error": str(e)}), 500
            
    @staticmethod
    def upload_avatar_to_cloudinary(file):
        try:
            upload_result = cloudinary.uploader.upload(
                file,
                folder="user_avatars",
                resource_type="image",
                overwrite=True
            )

            return upload_result.get('secure_url')
        
        
        except Exception as e:
            print(f"Erro ao fazer upload para Cloudinary: {e}")
            return None
        
    @staticmethod
    def delete_profile(userId):
        try:
            if not userId or userId == 'null' or userId == 'undefined':
                return jsonify({"error": "UserId é obrigatório"}), 400
            
            # Usar userId como string
            user_id_str = str(userId)

            #get Profile
            profile = UserProfile.query.filter_by(user_id=user_id_str).first()


            if not profile:
                return jsonify({'Error': 'Perfil não encontrado'}), 404
            
            CartItems.query.filter_by(user_id=user_id_str).delete(synchronize_session=False)
            Address.query.filter_by(client_user_id=user_id_str).delete(synchronize_session=False)
            ClientUser.query.filter_by(id=user_id_str).delete(synchronize_session=False)

           # User.query.filter_by(id=profile.user_id).delete()

            db.session.delete(profile)
            db.session.commit()

           

            db.session.commit()

            return jsonify({'message': 'Perfil removido com sucesso !'}), 200

        except Exception as e:
            db.session.rollback()
            print('Erro ao remover conta, tente novamente', e)
            return jsonify({"error": "Erro ao remover conta, tente novamente"}), 500