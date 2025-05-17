"Criar os objetos"

from app import db

#modelo do client
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #precisa ser único, como se fosse no login
    name = db.Column(db.String(100), index=True, unique=True)
    #precisa ser único
    email = db.Column(db.String(120), index=True, unique=True)

    def to_dict(self):
        # Cria um dicionário do objeto
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
    
#modelo do player
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    senha = db.Column(db.String, index=True) # verificar no git bruno
    initial_time = db.Column(db.Time, index=True)
    end_time = db.Column(db.time, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'initial_time': self.initial_time,
            'end_time': self.end_time
        }
