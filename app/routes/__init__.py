from flask import Blueprint

#Pega tem a mesma função do if main, porém, modularizar e organizar a aplicaçao Flask em componentes reutilizavéis
bp = Blueprint('main', __name__)

#from app.routes import clientes # encapsula as rotas de clients
#novas rotas precisam também ser encapsuladas nesse arquivo
