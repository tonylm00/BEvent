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

""" 
    CONTROLLO CARATTERI FORM REGISTRAZIONE
"""

email_valida = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
spec = ["$", "#", "@", "!", "*", "£", "%", "&", "/", "(", ")", "=", "|",
        "+", "-", "^", "_", "-", "?", ",", ":", ";", ".", "§", "°", "[", "]"]

def controlla_campi(nome, cognome, telefono, nome_utente,email, data_di_nascita):
    if not isinstance(nome, str)or not re.match(r'^[a-zA-ZÀ-ù ‘-]{2,30}$', nome):
        flash("Nome non valido", category="error")
    elif not isinstance(cognome, str) or not re.match(r'^[a-zA-ZÀ-ù ‘-]{2,30}$', nome):
        flash("Cognome non valido", category="error")
    elif not isinstance(nome_utente, str) or not 0 < len(nome_utente) <= 30:
        flash("Nome Utente non valido", category="error")
    elif not isinstance(telefono, str) or not len(telefono) == 10 or not telefono.isdigit():
        flash("Numero telefono non valido", category="error")
    elif not is_valid_email(email):
        flash("E-mail non valido", category="error")
    elif not is_valid_data_di_nascita(data_di_nascita):
        flash("Data di nascita non valida", category="error")
    else:
        return True
    return False
def is_valid_email(email):
    email_pattern=re.compile(r'''^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$''',re.VERBOSE)
    return bool(re.mach(email_pattern,email))
def is_valid_data_di_nascita(data_di_nascita):
    try:
        datetime_object = datetime.strptime(data_di_nascita, '%Y-%m-%d')
        return True
    except ValueError:
        return False



"""def registra_utente(nome,cognome,data_di_nascita, email,telefono, nome_utente,password,cpassword,isAdmin,Ruolo):
    if controlla_campi(nome,cognome,telefono,email,data_di_nascita, nome_utente):
"""
"""
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

    return False"""
