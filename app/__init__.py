"O __init__, diz que pasta é um diretório acessível, para executar comandos externos e rodar os comandos"
"é em um diretório python que serve para indicar ao interpretador python que o diretório deve ser tratado como um pacote"
"ele pode estar vázio ou pode conter o código de inicialização que é executado quando o pacote é importado, também utilizado como inicializador."

from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from app.db import db
from app.auth import token_required, auth_bp

#utilizado para migração do banco de dodos de forma dinâmica
#para manter o histórico de migrações
#automatiza a migração do modelo de dados com o banco de dados
migrate = Migrate()

def create_app(config_class=Config): #vem da classe que configuramos
    app = Flask(__name__)
    app.config.from_object(config_class) #vem da classe que configuramos

    #essa secret key é a nivel de aplicativo e a outra a nivel de rotas
    app.config['SECRET_KEY'] = 'your-secret-key'

    db.init_app(app)
    migrate.init_app(app, db) #executa o comando de migração de dados

    # o blue print de todas as rotas, vai ser encima do blueprint criado
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    #registra a autenticação e coloca o prefixo /auth
    app.register_blueprint(auth_bp, url_prefix='/auth')

    #tratamento de erro globais
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'message': 'unauthorized'}), 401
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message': 'internal server error'}), 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({'message': 'service unavailable'}), 503
    
    return app
        

