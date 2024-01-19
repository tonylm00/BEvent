from flask_login import UserMixin
from werkzeug.security import check_password_hash


class Utente(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.nome = user_data['nome']
        self.cognome = user_data['cognome']
        self.data_nascita = user_data['data_di_nascita']
        self.email = user_data['email']
        self.telefono = user_data['telefono']
        self.nome_utente = user_data['nome_utente']
        self.password_hash = user_data['password']
        self.ruolo = user_data['Ruolo']
        self.regione = user_data['regione']
        self.isAdmin = False

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
