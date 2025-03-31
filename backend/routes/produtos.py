from flask import Blueprint, request, jsonify
from database import db
from models.produto import Produto

produtos_bp = Blueprint("produtos", __name__)

@produtos_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{"id": p.id, "nome": p.nome, "descricao": p.descricao, "preco": p.preco} for p in produtos])

@produtos_bp.route("/produtos", methods=["POST"])
def adicionar_produto():
    data = request.json
    novo_produto = Produto(nome=data["nome"], descricao=data["descricao"], preco=data["preco"])
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({"mensagem": "Produto adicionado com sucesso!"})
