from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.address import Address
from database import db
from uuid import UUID as UUID_type

class AddressController:
    @staticmethod
    def get_address(user_id):
        print("Buscando endereços para user_id:", user_id)  # debug

        addresses = Address.query.filter_by(client_user_id=user_id).all()
        print(f"Registros encontrados: {len(addresses)}")  # debug

        address_list = []
        for addr in addresses:
            address_list.append({
                "id": addr.id,
                "cep": addr.cep,
                "logradouro": addr.logradouro,
                "numero": addr.numero,
                "complemento": addr.complemento,
                "bairro": addr.bairro,
                "cidade": addr.cidade,
                "estado": addr.estado,
                "pais": addr.pais,
                "referencia": addr.referencia,
                "created_at": addr.created_at,
                "updated_at": addr.updated_at
            })

        print("Endereços enviados:", address_list)  # debug
        return jsonify(address_list), 200

    @staticmethod
    @jwt_required()
    def create_address(user_id, data):
        try:
            user_uuid = UUID_type(str(user_id))

            # BUSCA SE EXISTE ENDEREÇO PARA ESSE USUÁRIO
            existing_address = Address.query.filter_by(client_user_id=user_uuid).first()

            # MAPEIA CAMPOS ACEITOS
            mapping = {
                'cep': 'cep',
                'logradouro': 'logradouro',
                'numero': 'numero',
                'complemento': 'complemento',
                'bairro': 'bairro',
                'cidade': 'cidade',
                'estado': 'estado',
                'pais': 'pais',
                'referencia': 'referencia'
            }

            if existing_address:
                # ATUALIZA APENAS O QUE EXISTE
                for key, model_field in mapping.items():
                    if key in data and data[key] is not None:
                        setattr(existing_address, model_field, data[key])

                db.session.commit()
                return {
                    "message": "Endereço atualizado com sucesso!",
                    "address": existing_address.to_dict()
                }

            # CRIA NOVO
            new_address = Address(
                client_user_id=user_uuid,
                **{
                    model_field: data.get(key)
                    for key, model_field in mapping.items()
                }
            )

            db.session.add(new_address)
            db.session.commit()

            return {
                "message": "Endereço criado com sucesso!",
                "address": new_address.to_dict()
            }

        except Exception as e:
            db.session.rollback()
            return {"error": f"Erro ao processar endereço: {str(e)}"}

    @staticmethod
    def update_address(user_id, address_id, data):
        try:
            user_uuid = UUID_type(str(user_id))
            address = Address.query.filter_by(id=address_id, client_user_id=user_uuid).first()
            if not address:
                return {"error": "Endereço não encontrado", "address": None}

            field_map = {
                'zip': 'cep',
                'street': 'logradouro',
                'number': 'numero',
                'complement': 'complemento',
                'neighborhood': 'bairro',
                'city': 'cidade',
                'state': 'estado',
                'country': 'pais',
                'reference': 'referencia'
            }

            for key, value in data.items():
                mapped_key = field_map.get(key, key)  # usa key original se não estiver no map
                if hasattr(address, mapped_key) and value is not None:
                    setattr(address, mapped_key, value)

            
            db.session.commit()
            return {"message": "Endereço atualizado com sucesso!", "address": address.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {"error": f"Erro ao atualizar endereço: {str(e)}"}

    @staticmethod
    def delete_address(address_id, user_id):
       
        address = Address.query.filter_by(id=address_id, client_user_id=user_id).first()
        if not address:
            return jsonify({"error": "Endereço não encontrado"})
        
        try:
            db.session.delete(address)
            db.session.commit()
            return jsonify({"message": "Endereço deletado com sucesso."}), 200
        except Exception as e:
            return jsonify({"error": "Erro ao deletar endereço", "details": str(e)}), 500