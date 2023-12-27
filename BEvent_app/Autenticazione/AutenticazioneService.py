import hashlib

from flask import flash
import re
from flask import Flask, flash
from pymongo import MongoClient, collection
from werkzeug.security import generate_password_hash, check_password_hash

from BEvent_app.Routes import ruolo_utente

# import hashlib

client = MongoClient('mongodb://localhost:27017/')
db = client['BEvent']
users_collection = db['Utente']


# def hash_password(password):
#    return hashlib.sha256(password.encode()).hexdigest()


def verify_user(email, password):
    user = users_collection.find_one({'email': email, 'password': password})
    return user


""" 
    CONTROLLO CARATTERI FORM REGISTRAZIONE
"""

email_valida = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
spec = ["$", "#", "@", "!", "*", "£", "%", "&", "/", "(", ")", "=", "|",
        "+", "-", "^", "_", "-", "?", ",", ":", ";", ".", "§", "°", "[", "]"]


def controlla_campi(nome, cognome, telefono, nome_utente, email, data_di_nascita):
    if not isinstance(nome, str) or not re.match(r'^[a-zA-ZÀ-ù ‘-]{2,30}$', nome):
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
    email_pattern = re.compile(r'''^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$''', re.VERBOSE)
    return bool(re.match(email_pattern, email))


def is_valid_data_di_nascita(data_di_nascita):
    try:
        datetime_object = datetime.strptime(data_di_nascita, '%d-%m-%Y')
        return True
    except ValueError:
        return False


def controlla_password(password):
    if not isinstance(password, str) or len(password) < 8:
        flash("Lunghezza non valida", "error")
    else:
        # Utilizza l'espressione regolare per convalidare il formato della password
        regex_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if not re.match(regex_pattern, password):
            flash("Formato non valido", "error")
        else:
            # La password è valida
            return True
    return False


def conferma_password(password, cpassword):
    if password == cpassword:
        return True
    return False


def registra_org(nome, cognome, nome_utente, email, password, cpassword, telefono, data_di_nascita, citta, ruolo):
    if controlla_campi(nome, cognome, telefono, nome_utente, email, data_di_nascita):
        if not is_valid_email(email):
            flash("Email esistente", "error")
        elif not controlla_password(password):
            flash("Password non valida", "error")
        elif not conferma_password(password, cpassword):
            flash("Le password non corrispondono", "error")
        else:
            hashed_password = generate_password_hash(password, method='sha256')
            user_document = {
                "nome": nome,
                "cognome": cognome,
                "data_di_nascita": data_di_nascita,
                "email": email,
                "telefono": telefono,
                "nome_utente": nome_utente,
                "password": hashed_password,
                "Admin": {
                    "isAdmin": False
                },
                "Ruolo": ruolo,
                "Organizzatore": {
                    "FotoOrganizzatore": "",
                    "Citta": citta
                }
            }
            users_collection.insert_one(user_document)
            flash("Registrazione avvenuta con successo!", "success")
            return True
    return False
