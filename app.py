from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jogo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ======================================
# MODELOS DO BANCO DE DADOS
# ======================================
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(50), unique=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    eh_administrador = db.Column(db.Boolean, default=False)

    def para_json(self):
        return {
            'id': self.id,
            'nome': self.nome_usuario,
            'admin': self.eh_administrador
        }

class SessaoJogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tabuada_selecionada = db.Column(db.Integer, nullable=False)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime)
    pontuacao = db.Column(db.Integer, default=0)
    vidas_restantes = db.Column(db.Integer, default=3)
    tipo_estrela = db.Column(db.String(20))

    def calcular_estrela(self):
        tempo_decorrido = (datetime.utcnow() - self.data_inicio).total_seconds()
        
        if tempo_decorrido < 60 and self.vidas_restantes >= 3:
            return 'diamante'
        elif tempo_decorrido < 90 and self.vidas_restantes >= 2:
            return 'ouro'
        elif tempo_decorrido < 120 and self.vidas_restantes >= 1:
            return 'prata'
        return 'bronze'

class Dica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tabuada_relacionada = db.Column(db.Integer, nullable=False)
    texto_dica = db.Column(db.String(500), nullable=False)

    @staticmethod
    def obter_dica_aleatoria(tabuada):
        dicas = Dica.query.filter_by(tabuada_relacionada=tabuada).all()
        return random.choice(dicas) if dicas else None

# ======================================
# ROTAS DA API
# ======================================
class RotasUsuarios:
    @app.route('/api/usuarios', methods=['POST'])
    def criar_usuario():
        dados = request.get_json()
        novo_usuario = Usuario(nome_usuario=dados['nome'])
        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify(novo_usuario.para_json()), 201

class RotasJogo:
    @app.route('/api/sessoes', methods=['POST'])
    def iniciar_sessao():
        dados = request.get_json()
        sessao = SessaoJogo(
            id_usuario=dados['id_usuario'],
            tabuada_selecionada=dados['tabuada']
        )
        db.session.add(sessao)
        db.session.commit()
        return jsonify({'id_sessao': sessao.id}), 201

    @app.route('/api/sessoes/<int:id_sessao>', methods=['PUT'])
    def finalizar_sessao(id_sessao):
        sessao = SessaoJogo.query.get(id_sessao)
        dados = request.get_json()
        
        sessao.pontuacao = dados['pontuacao']
        sessao.vidas_restantes = dados['vidas']
        sessao.tipo_estrela = sessao.calcular_estrela()
        sessao.data_fim = datetime.utcnow()
        
        db.session.commit()
        return jsonify({
            'estrela': sessao.tipo_estrela,
            'pontuacao_final': sessao.pontuacao
        })

class RotasAjuda:
    @app.route('/api/dicas/<int:tabuada>', methods=['GET'])
    def obter_dica(tabuada):
        dica = Dica.obter_dica_aleatoria(tabuada)
        return jsonify({'dica': dica.texto_dica}) if dica else ('', 404)

# ======================================
# FUNÇÕES AUXILIARES
# ======================================
class InicializadorBD:
    @staticmethod
    def popular_dicas():
        dicas_base = [
            (7, "Multiplique por 10 e subtraia três vezes o número: 7×7 = (7×10) - (7×3) = 70-21 = 49"),
            (8, "Dobrar três vezes: 8×4 = 8+8=16 → 16+16=32"),
            # Adicionar mais dicas conforme necessário
        ]
        
        for tabuada, texto in dicas_base:
            if not Dica.query.filter_by(texto_dica=texto).first():
                db.session.add(Dica(
                    tabuada_relacionada=tabuada,
                    texto_dica=texto
                ))
        db.session.commit()

    @staticmethod
    def criar_admin_inicial():
        if not Usuario.query.filter_by(eh_administrador=True).first():
            admin = Usuario(
                nome_usuario='AdminPrincipal',
                eh_administrador=True
            )
            db.session.add(admin)
            db.session.commit()

# ======================================
# CONFIGURAÇÃO INICIAL
# ======================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        InicializadorBD.popular_dicas()
        InicializadorBD.criar_admin_inicial()
    app.run(debug=True)