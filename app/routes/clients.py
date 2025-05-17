"Conter as rotas para o cliente"

from flask import jsonify, request, abort
from app import db
from app.models import Client
from app.routes import bp
from app.auth import token_required

@bp.route('/clients', methods=['GET'])
@token_required #rota só funciona se tiver um token de autenticação
def get_clients(current_user): # É o usuário atual, o que fez a requisição, é um padrão
    client_id = request.args.get('client_id') #Buscando pelo client id nos argumentos da requisição

    #se existir client id
    if client_id:
        try:
            client = Client.query.get_or_404(client_id)
            return jsonify(client.to_dict()), 200 #HTTP ok
        except Exception as e:
            return jsonify({'error': str(e)}), 500 #erro de servidor
    else: #caso contrário, retorna todos
        try:
            clients = Client.query.all()
            #retorna um array com todos os clientes
            return jsonify([client.to_dict() for client in clients]), 200 # http ok
        except Exception as e:
            return jsonify({'error': str(e)}), 500 #erro de servidor 
            
@bp.route('/clients', methods=['POST'])
@token_required
def create_cliente(current_user):
    try:
        data = request.get_json() or {} #recupera em json, ou aceita o que está sendo enviado
        if 'name'not in data or 'email' not in data:
            return jsonify({'error': 'name and email are required'}), 400 #bad request
        if Client.query.filter_by(name=data['name']).first(): #se já existir nome, retorna erro
            return jsonify({'erro': 'name already registered'}), 400
        if Client.query.filter_by(email=data['email']).first(): # se já existir email, retorna erro
            return jsonify({'erro': 'email already registered'}), 400
        
        #salva no banco
        client = Client(name=data['name'], email=data['email'])
        db.session.add(client)
        db.session.commit()
        return jsonify(client.to_dict()), 201 #sucesso na criação
    except Exception as e:
        return jsonify({'error': str(e)}), #erro de servidor

#exemplo de PUT
@bp.route('/clients/<int:id>', methods=['PUT'])
@token_required
def update_client(current_user, id):
    try:
        client = Client.query.get_or_404(id)
        data = request.get_json() or {} #recupera em json, ou aceita o que está sendo enviado

        if 'name' not in data or 'email' not in data:
            return jsonify({'error': 'name and email are required'}), 400 #bad request
        if Client.query.filter_by(name=data['name']).first(): #se já existir nome, retorna erro
            return jsonify({'erro': 'name already registered'}), 400
        if Client.query.filter_by(email=data['email']).first(): # se já existir email, retorna erro
            return jsonify({'erro': 'email already registered'}), 400
        
        #salva no banco
        client.name = data['name']
        client.email = data['email']
        db.session.add(client)
        db.session.commit()
        return jsonify(client.to_dict()), 200 #sucesso na criação
    except Exception as e:
        return jsonify({'error': str(e)}), 500 #erro de servidor
    
#exemplo de DELETE
@bp.route('/clients/<int:id>', methods=['DELETE'])
@token_required
def delete_cliente(current_user, id):
    try:
        client = Client.query.get_or_404(id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Sucesso delete client'}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
            