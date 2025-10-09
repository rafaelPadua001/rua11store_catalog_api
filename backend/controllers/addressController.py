from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.address import Address
from database import db
import uuid

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
    def create_address():
        try:
            user_id = get_jwt_identity()
            data = request.json

            # Verifica se já existe endereço para esse usuário
            address = Address.query.filter_by(client_user_id=user_id).first()

            if address:
                # Atualiza os campos existentes
                address.cep = data['cep']
                address.logradouro = data['logradouro']
                address.numero = data['numero']
                address.complemento = data.get('complemento')
                address.bairro = data['bairro']
                address.cidade = data['cidade']
                address.estado = data['estado']
                address.pais = data.get('pais', 'Brasil')
                address.referencia = data.get('referencia')
                db.session.commit()
                return jsonify({"message": "Endereço atualizado com sucesso", "address_id": address.id}), 200

            else:
                # Cria novo endereço
                from uuid import uuid4
                new_address = Address(
                    client_user_id=user_id,
                    cep=data['cep'],
                    logradouro=data['logradouro'],
                    numero=data['numero'],
                    complemento=data.get('complemento'),
                    bairro=data['bairro'],
                    cidade=data['cidade'],
                    estado=data['estado'],
                    pais=data.get('pais', 'Brasil'),
                    referencia=data.get('referencia')
                )
                db.session.add(new_address)
                db.session.commit()
                return jsonify({"message": "Endereço salvo com sucesso", "address_id": new_address.id}), 201

        except KeyError as e:
            return jsonify({"error": f"Campo obrigatório faltando: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @staticmethod
    def update_address(user_id, address_id, data):
        address = Address.query.filter_by(id=address_id, client_user_id=user_id).first()

        if not address:
            return {"error": "Endereço não encontrado"}, 404
        
        for key, value in data.items():
            if hasattr(address, key) and value is not None:
                setattr(address, key, value)

        db.session.commit()
        return {"message": "Endereço atualizado com sucesso!", "address": address.to_dict() if hasattr(address, 'to_dict') else data}
    
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