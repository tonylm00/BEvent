from datetime import datetime
import re
from bson import ObjectId
from flask import flash

from ..InterfacciaPersistenza.Biglietto import Biglietto
from ..InterfacciaPersistenza.EventoPubblico import Evento_Pubblico
from ..InterfacciaPersistenza.Utente import Utente
from ..InterfacciaPersistenza.Organizzatore import Organizzatore
from ..InterfacciaPersistenza.Fornitore import Fornitore
from ..InterfacciaPersistenza.Admin import Admin
from ..InterfacciaPersistenza.EventoPrivato import Evento_Privato
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

        if utente.check_password(password):
            print("prova")
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


def is_valid_email(email):
    email_pattern = re.compile(r'''^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$''', re.VERBOSE)
    return bool(re.match(email_pattern, email))


def is_valid_data_di_nascita(data):
    try:
        datetime_data = datetime.strptime(data, '%Y-%m-%d')
        data_odierna = datetime.now()
        if datetime_data < data_odierna:
            return True
        else:
            return False

    except ValueError:
        return False


def controlla_password(password):
    if not isinstance(password, str) or len(password) < 8:

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
    data_formattata = datetime.strptime(data_di_nascita, "%Y-%m-%d").strftime("%d-%m-%Y")
    user_data = None
    if ruolo == "1":
        user_data = {
            '_id': ObjectId(),
            'nome': nome,
            'cognome': cognome,
            'data_di_nascita': data_formattata,
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
            '_id': ObjectId(),
            'nome': nome,
            'cognome': cognome,
            'data_di_nascita': data_formattata,
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


def registra_org(nome, cognome, nome_utente, email, password, cpassword, telefono, data_di_nascita, citta, ruolo,
                 regione):
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

            organizzatore_data = {
                'Organizzatore': {
                    'FotoOrganizzatore': "",
                    'Citta': citta
                }
            }

            documento_organizzatore = {**user_data, **organizzatore_data}
            organizzatore = Organizzatore(user_data, organizzatore_data)

            db.Utente.insert_one(documento_organizzatore)

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
                    'Foto': [],
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


def get_dati_area_organizzatore(id_organizzatore):
    db = get_db()
    organizzatore_data = db['Utente'].find_one({'_id': ObjectId(id_organizzatore)})
    organizzatore = Organizzatore(organizzatore_data, organizzatore_data)

    eventi_privati_data = list(db['Evento'].find({
        'Organizzatore': id_organizzatore,
        'Ruolo': "2"
    }))
    eventi_privati = []
    for data in eventi_privati_data:
        evento_privato = Evento_Privato(data, data)
        eventi_privati.append(evento_privato)

    biglietti_comprati_data = list(db['Biglietto'].find({
        'Comprato_da': id_organizzatore
    }))
    biglietti_comprati = []
    for data in biglietti_comprati_data:
        biglietto = Biglietto(data)
        biglietti_comprati.append(biglietto)

    return organizzatore, eventi_privati, biglietti_comprati



def get_dati_home_organizzatore(id_organizzatore):
    db = get_db()
    data_odierna = datetime.now().strftime("%d-%m-%Y")

    query = {
        "Ruolo": "2",
        "EventoPrivato.Organizzatore": id_organizzatore,
        "Data": {"$gte": data_odierna},
    }
    try:
        evento_data = db['Evento'].find(query).sort("Data", 1).limit(1).next()
        evento_privato = Evento_Privato(evento_data, evento_data)
    except StopIteration:
        evento_data = None
        evento_privato = None

    query = {
        "Ruolo": "1",
        "Data": {"$gte": data_odierna},
        "isPagato": True
    }

    evento_pubblico_data = db['Evento'].find(query).sort("Data", 1).limit(4)
    if evento_pubblico_data:
        eventi_pubblici = []
        for data in evento_pubblico_data:
            evento_pubblico = Evento_Pubblico(data, data)
            eventi_pubblici.append(evento_pubblico)
    else:
        query = {
            "Ruolo": "1",
            "Data": {"$gte": data_odierna},
            "isPagato": False
        }
        evento_pubblico_data = db['Evento'].find(query).sort("Data", 1).limit(2)
        eventi_pubblici = []
        for data in evento_pubblico_data:
            evento_pubblico = Evento_Pubblico(data, data)
            eventi_pubblici.append(evento_pubblico)

    return evento_privato, eventi_pubblici
