from datetime import datetime
import re
from bson import ObjectId
from flask import flash
from ..InterfacciaPersistenza.Utente import Utente
from ..InterfacciaPersistenza.Organizzatore import Organizzatore
from ..InterfacciaPersistenza.Fornitore import Fornitore
from BEvent_app.InterfacciaPersistenza.Admin import Admin
from ..db import get_db
from werkzeug.security import generate_password_hash


def verify_user(email, password):
    db = get_db()
    user_data = db.Utente.find_one({'email': email})

    if user_data:
        utente = Utente(user_data)
        if user_data['Ruolo'] == "1":
            utente = Admin(user_data)
        elif user_data['Ruolo'] == "2":
            utente = Organizzatore(user_data, user_data)
        elif user_data['Ruolo'] == "3":
            utente = Fornitore(user_data, user_data)

        # if utente.check_password(password):
        return utente  # Ritorna l'istanza dell'utente
    else:
        return None


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
        print("prova registrazione11")
        flash("Lunghezza non valida", "error")
    else:
        # Utilizza l'espressione regolare per convalidare il formato della password
        regex_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$'

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


def crea_doc_utente(password, ruolo, nome, cognome, nome_utente, email, telefono, data_di_nascita, regione):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    user_data = None
    if ruolo == "1":
        user_data = {
            '_id': ObjectId(),  # Genera un nuovo ObjectId
            'nome': nome,
            'cognome': cognome,
            'data_di_nascita': data_di_nascita,
            'email': email,
            'telefono': telefono,
            'nome_utente': nome_utente,
            'password': hashed_password,
            "Admin": {
                "isAdmin": True
            },
            'Ruolo': ruolo
        }
    else:
        user_data = {
            '_id': ObjectId(),  # Genera un nuovo ObjectId
            'nome': nome,
            'cognome': cognome,
            'data_di_nascita': data_di_nascita,
            'email': email,
            'telefono': telefono,
            'nome_utente': nome_utente,
            'password': hashed_password,
            "Admin": {
                "isAdmin": False
            },
            'Ruolo': ruolo,
            'regione': regione
        }

    return user_data


def registra_org(nome, cognome, nome_utente, email, password, cpassword, telefono, data_di_nascita, citta, ruolo, regione):
    db = get_db()
    print("prova registrazione")
    if controlla_campi(nome, cognome, telefono, nome_utente, email, data_di_nascita):
        print("prova registrazione2")
        if not is_valid_email(email):
            print("prova registrazione6")
            flash("Email esistente", "error")
        elif not controlla_password(password):
            print("prova registrazione7")
            flash("Password non valida", "error")
        elif not conferma_password(password, cpassword):
            print("prova registrazione8")
            flash("Le password non corrispondono", "error")
        else:
            print("prova registrazione10")
            user_data = crea_doc_utente(password, ruolo, nome, cognome, nome_utente, email, telefono, data_di_nascita,
                                        regione)

            organizzatore_data = {
                'Organizzatore': {
                    'FotoOrganizzatore': "",
                    'Citta': citta
                }
            }

            documento_organizzatore = {**user_data, **organizzatore_data}
            organizzatore = Organizzatore(user_data, organizzatore_data)
            print("prova registrazione3")
            db.Utente.insert_one(documento_organizzatore)
            print("prova registrazion4")
            flash("Registrazione avvenuta con successo!", "success")

            return organizzatore
    return None


def registra_forn(nome, cognome, nome_utente, email, password, cpassword, telefono, data_di_nascita, citta, ruolo,
                  descrizione, islocation, eventi_max_giorn, via, piva, regione):
    db = get_db()
    if controlla_campi(nome, cognome, telefono, nome_utente, email, data_di_nascita):
        if not is_valid_email(email):
            flash("Email esistente", "error")
        elif not controlla_password(password):
            flash("Password non valida", "error")
        elif not conferma_password(password, cpassword):
            flash("Le password non corrispondono", "error")
        else:

            user_data = crea_doc_utente(password, ruolo, nome, cognome, nome_utente, email, telefono, data_di_nascita,
                                        regione)

            fornitore_data = {
                'Fornitore': {
                    'Descrizione': descrizione,
                    'EventiMassimiGiornaliero': eventi_max_giorn,
                    'OrarioDiLavoro': "",
                    'Foto': "",
                    'Citta': citta,
                    'Via': via,
                    'Partita_Iva': piva,
                    'isLocation': islocation
                }
            }

            documento_fornitore = {**user_data, **fornitore_data}
            fornitore = Fornitore(user_data, fornitore_data)

            db.Utente.insert_one(documento_fornitore)
            flash("Registrazione avvenuta con successo!", "success")

            return fornitore
    return None


def registra_admin(nome, cognome, nome_utente, email, password, cpassword, telefono, data_di_nascita, ruolo, regione):
    db = get_db()
    if controlla_campi(nome, cognome, telefono, nome_utente, email, data_di_nascita):
        if not is_valid_email(email):
            flash("Email esistente", "error")
        elif not controlla_password(password):
            flash("Password non valida", "error")
        elif not conferma_password(password, cpassword):
            flash("Le password non corrispondono", "error")
        else:
            user_data = crea_doc_utente(password, ruolo, nome, cognome, nome_utente, email, telefono, data_di_nascita,
                                        regione)

            documento_admin = {**user_data}
            admin = Admin(user_data)
            db.Utente.insert_one(documento_admin)

            flash("Registrazione avvenuta con successo!", "success")
            return Admin
    return None
