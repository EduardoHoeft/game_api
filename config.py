"armazena configurações de todo projeto"

import os

#cria uma variável de caminho relativo para o projeto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #A secret key é um valor armazenado em um arquivo .env do projeto
    #O password é para utilizar em ambientes de teste
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #caminho do banco
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "app.db")
    #Realizar track de alterações, por enquanto não vamos usar mas sempre devemos configurar
    SQLALCHEMY_track_modifications = False
    