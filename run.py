"Não usa o main, será utilizado o run.py, entra como se fosse um shell de inicialização do server"

from app import create_app, db
from app.models import Client, Player

#criando o aplicativo
app = create_app()

#O trecho configura um processador de contexto shell
#Este processador torna certo objetos disponíveis no shell do Flask sem a necessidade de importá-los manualmente
#Utilizaremos o comando "flask run" para rodar a aplicação
@app.shell_context_processor
def make_shell_context():
    #Retorna um dicionário com as chaves 'db' e 'Cliente', para que a instância db e o modelo Cliente disponíveis no shell
    return {'db': db, 'Client': Client,
            'db': db, 'Player': Player
            }
