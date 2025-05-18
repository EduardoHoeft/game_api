from flask import jsonify, request
from app import db
from app.models import Player
from app.routes import bp
from app.auth import token_required
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

@bp.route('/players', methods=['GET'])
@token_required # token de autenticação
def get_players(current_user):
    player_id = request.args.get('player_id')

    if player_id:
        try:
            players = Player.query.get_or_404(player_id)
            return jsonify(Player.to_dict()), 200 # OK
        except Exception as e:
            return jsonify({'error': str(e)}), 500 #erro de servidor
    else: #caso contrário, retorna todos
        try:
            player = Player.query.all()
            #retorna um array com todos os players
            return jsonify([player.to_dict() for player in players]), 200 # http OK
        except Exception as e:
            return jsonify({'error': str(e)}), 500 #erro de servidor
        
@bp.route('/players', methods=['POST'])
@token_required
def create_player(current_user):
    
    try:
        data = request.get_json() or {} #recupera em json, ou aceita o que está sendo enviado
        if 'name' not in data or 'email' not in data:
            return jsonify({'error': 'name and email are required'}), 400 #bad request
        if Player.query.filter_by(name=data['name']).first(): #se já existir nome, retorna erro
            return jsonify({'error': 'name already registered'}), 400
        if Player.query.filter_by(email=data['email']).first(): # se já existir email, retorna erro
            return jsonify({'error': 'email already registered'}), 400
        
        #gera um hash
        hashed_password = generate_password_hash(data['senha'])
        
        #salva no banco
        player = Player(
            name=data['name'],
            email=data['email'],
            senha_hash=hashed_password,
            initial_time=data.get('initial_time'),
            end_time=data.get('end_time')
        )
        db.session.add(player)
        db.session.commit()

        return jsonify(player.to_dict()), 201 #sucesso na criação
    except Exception as e:
        return jsonify({'error': str(e)}), #erro de servidor

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        if 'email' not in data or 'senha' not in data:
            return jsonify({'error': 'email and password are required'}), 400

        user = Player.query.filter_by(email=data['email']).first()

        if not user or not check_password_hash(user.senha, data['senha']):
            return jsonify({'error': 'Invalid email or password'}), 401

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, 'SECRET_KEY', algorithm='HS256')

        return jsonify({'token': token}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@bp.route('/players/<int:id>', methods=['PUT'])
@token_required
def update_client(current_user, id):
    player = Player.query.get_or_404(id)

    if current_user.id != player.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}

    if 'name' in data:
        existing_user = player.query.filter_by(name=data['name']).first()
        if existing_user and existing_user.id != player.id:
            return jsonify({'error': 'Username already exists.'}), 400
        player.name = data['name']

    if 'senha' in data:
        player.senha = generate_password_hash(data['senha'])

    if 'name' in data:
        player.name = data['name']
    if 'email' in data:
        player.email = data['email']
    if 'initial_time' in data:
        player.intial_time = data['initial_time']
    if 'end_time' in data:
        player.end_time = data['end_time']

    db.session.commit()
    return jsonify(player.to_dict()), 200

@bp.route('/players/<int:id>', methods=['DELETE'])
@token_required
def delete_cliente(current_user, id):
    try:
        player = Player.query.get_or_404(id)
        db.session.delete(player)
        db.session.commit()
        return jsonify({'message': 'Sucesso delete client'}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

