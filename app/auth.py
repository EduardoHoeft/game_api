"Utilizada para autenticação JWT"

import datetime
import jwt
#para envolver ou encapsular algo dentro de uma outra função, ou seja, chamar com o @
from functools import wraps
from flask import request, jsonify, Blueprint, current_app

#O blueprint do flask organizar uma aplicação flask em componentes menores e reutilizáveis
#É útil para grandes aplicações por facilitar a manutenção, modularização e reutilização do código
#Com ele: organizamos o código, reutilização de código (em outros projetos),
#gestão de roteamento (ter suas próprias rotas, como rota de autenticação, rotas de api, rotas de adiministração, entre outras rotas),
#e modularização(divisão da aplicação em partes independentes e autônomas)

auth_bp = Blueprint('auth', __name__)
#Esse código é apenas para autenticação e não será utilizada em outra parte do código

@auth_bp.route('/login', methods=['post'])
def ogin():
    auth_data = request.get_json() #Blueprint já tem encapsulado
    username = auth_data.get('username')
    password = auth_data.get('password')

    if username == "admin" and password == "password":
        # aqui deveria ser uma consulta na database, mas vamos deixar apenas com if para fins didáticos
        #crie sua própria busca no banco

        token = jwt.encode(
            {
                'user': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                #conjunto mínimo de parâmetros necessários
            },
            current_app.config["SECRET_KEY"], #definido o config.py, e chamando automaticamente
            algorithm='HS256'
        )
        return jsonify({'token': token}), 200 #tudo ok
    return jsonify({'message': 'Invalid username or password'}), 401 #erro de autenticação

#criando a marcação das rotas. A função será encapsulada dentro do método decorated
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None #inicializa como vázio

        #vamos exigir que o token esteja no header
        #Tokens armazenados em cabeçalhos são menos suscetíveis a ataques de Cross-Site Request Forgery (CSRF)
        #Cabeçalhos de autorização não são facilmente visíveis e manipulaveis pelo javascript do lado do cliente
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if not token:
                return jsonify({'message': 'Token is missing'}), 401 #erro de autenticação
            
            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])
                current_user = data['user'] # cria o user que será utilizado nas rotas
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token is expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token is invalid'}), 401

            return f(current_user, *args, **kwargs)
        return decorated
    