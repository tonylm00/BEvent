import hashlib
from pymongo import MongoClient, collection
from werkzeug.security import generate_password_hash

from BEvent_app.Routes import ruolo_utente

# import hashlib

client = MongoClient('mongodb://localhost:27017/')
db = client['BEvent']
users_collection = db['Utente']


#def hash_password(password):
#    return hashlib.sha256(password.encode()).hexdigest()


def verify_user(email, password):
    user = users_collection.find_one({'email': email, 'password': password})
    return user


def ruolo(email):
    user = users_collection.find_one({'email': email})
    if user:
        ruolo = user.get('ruolo', None)
        return ruolo
    return None


def registra_utente(nome,cognome,nome_utente,email,password,cpassword,telefono,indirizzo,tipo):
    if controlla_campi(nome,cognome,indirizzo,telefono,email):
        if not controlla_email_esistente(email):
            flash("Email esistente", category="error")
        elif contolla_password (password,cpassword):
            if (tipo='Fornitore'):
                user= Fornitore(nome=nome, cognome=cognome,nome_utente=nome_utente,email=email,telefono=telefono,indirizzo=indirizzo,password=generate_password_hash(password,method='sha256'))
            else:
                user= Organizzatore(#tutte le cose di organizzatore)
            db.session.add(user)
            db.session.commit()
            login_user(user)
    return False
