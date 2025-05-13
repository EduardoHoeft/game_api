#arquivo principal

#import
from flask import Flask

#instancia do site em flask para uma variável
app = Flask(__name__)

#rota principal
@app.route("/")
def teste():
    return "OK - funcionando"

# sempre ficar abaixo das rotas se não erro 404
app.run(debug=True) # debug=true ativa modo depuração.