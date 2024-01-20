from datetime import datetime
import re
from bson import ObjectId
from flask import flash
from ..InterfacciaPersistenza.Biglietto import Biglietto
from ..InterfacciaPersistenza.EventoPubblico import EventoPubblico
from ..InterfacciaPersistenza.Utente import Utente
from ..InterfacciaPersistenza.Organizzatore import Organizzatore
from ..InterfacciaPersistenza.Fornitore import Fornitore
from ..InterfacciaPersistenza.Admin import Admin
from ..InterfacciaPersistenza.EventoPrivato import EventoPrivato
from ..db import get_db
from werkzeug.security import generate_password_hash

db = get_db()


def verify_user(email, password):
    """verifica l'email e la password forniti dall'utente nel sistema
    Parameters:
        email(str):email da verificare.
        password(str):password da verificare
    Return:
        restituisce un'istanza dell'utente se la verifica ha successo, altrimenti None
        """

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


def controlla_campi(nome, cognome, telefono, nome_utente, email, data_di_nascita, piva):
    """
    controlla la validità dei campi utente e segna eventuali errori utilizzando flash
    :param nome: (str) Nome dell'utente
    :param cognome: (str) Cognome dell'utente
    :param telefono:(str) Numero di telefono dell'utente
    :param nome_utente: (str) Nome utente dell'utente
    :param email: (str) indirizzo email dell'utente
    :param data_di_nascita: (str) data di nascita dell'utente con il formato anno-mese-giorno

    :return:True se tuttii i campi sono validi, altrimenti restituisce None
    """
    if not isinstance(nome, str) or not re.match(r'^[a-zA-ZÀ-ù ‘-]{2,30}$', nome):

        return False, "Nome non valido"

    elif not isinstance(cognome, str) or not re.match(r'^[a-zA-ZÀ-ù ‘-]{2,30}$', cognome):

        return False, "Cognome non valido"

    elif not isinstance(nome_utente, str) or not 0 < len(nome_utente) <= 30:

        return False, "Nome Utente non valido"

    elif not isinstance(telefono, str) or not len(telefono) == 10 or not telefono.isdigit():

        return False, "Numero telefono non valido"
    elif not isinstance(piva, str) or not len(piva) == 11 or not piva.isdigit():

        return False, "Partita iva non valida"


    elif not is_valid_email(email):

        return False, "E-mail non valido"

    elif not is_valid_data_di_nascita(data_di_nascita):

        return False, "Data di nascita non valida"

    else:
        return True, "Controllo riuscito"


def is_valid_email(email):
    """
    verifica se un indirizzo email è valido o no
    :param email: (str) indirizzo email da verificare
    :return: restituisce True se l'indirizzo email è valido, altrimenti restituisce False
    """
    email_pattern = re.compile(r'''^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$''', re.VERBOSE)
    return bool(re.match(email_pattern, email))


def is_valid_data_di_nascita(data):
    """
    verifica se la data di nascita inserita dall'utente è valida o no
    :param data: (str) data di nascita nel normato anno-mese-giorno
    :return: restituisce True se la data di nascita è valida e precede la data odierna, altrimenti restituisce False
    """

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
    """
    Verifica la validità di una password
    la password deve soddisfarre i seguenti requisiti:
    - lunghezza di 8caratteri minimo
    - contenere almeno una lettera minuscola
    - contenere almeno una lettera maiuscola
    - contenere almeno un numero
    - contenere almeno un carattere speciale tra '@','$','!','%','*','?','&','.'
    :param password: (str) password da verificare
    :return: restituisce true se la password è valida, altrimenti c'è un messaggio di errore e restituisce False
    """
    if not isinstance(password, str) or len(password) < 8:
        return False, "Lunghezza non valida"

    else:
        # Utilizza l'espressione regolare per convalidare il formato della password
        regex_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$'

        if not re.match(regex_pattern, password):
            return False, "Formato non valido"

        else:
            # La password è valida
            return True, "Formato valido"


def conferma_password(password, cpassword):
    """
    Conferma se la conferma password corrisponde alla password precedentemente inserita
    :param password: (str) prima password da confrontare
    :param cpassword: (str) seconda password da confrontare
    :return: Restituisce true se le due password corrispondono, altrimenti restituisce False
    """
    if password == cpassword:
        return True
    return False


def crea_doc_utente(password, ruolo, nome, cognome, nome_utente, email, telefono, data_di_nascita, regione):
    """
    Crea un documento utente con i dati dell'utente
    :param password: (str) password dell'utente
    :param ruolo: (str) il ruolo dell'utente (1 per Admin,2 Organizzatore, 3 Fornitore)
    :param nome: (str) nome dell'utente
    :param cognome: (str) cognome dell'utente
    :param nome_utente: (str) nome utente dell'utente
    :param email: (str) email dell'utente
    :param telefono: (str) telefono dell'utente
    :param data_di_nascita: (str) data di nascita dell'utente
    :param regione:(str or None) regione dell'utente
    :return: Restituisce un documento dei dati dell'utente
    """
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


def registra_forn(nome, cognome, nome_utente, email, password, cpassword, telefono, data_di_nascita, citta, ruolo,
                  descrizione, islocation, eventi_max_giorn, via, piva, regione):
    """
    Registra un fornitore nel sistema
    :param nome: (str) nome del fornitore
    :param cognome: (str) cognome del fornitore
    :param nome_utente: (str) nome utente del fornitore
    :param email: (str) email del fornitore
    :param password: (str) password del fornitore
    :param cpassword: (str) conferma password del fornitore
    :param telefono: (str) numero di telefono del fornitore
    :param data_di_nascita: (str) data di nascita del fornitore nel formato 'YYYY-MM-DD'
    :param citta: (str) città del fornitore
    :param ruolo: (int) il ruolo per confermare che è un fornitore
    :param descrizione:(str) descrizione del fornitore
    :param islocation: (bool) indica se il fornitore è una location o no
    :param eventi_max_giorn: (int) numero massimo di eventi che un fornitore può gestire al giorno
    :param via: (str) via del fornitore
    :param piva: (str) partita IVA del fornitore
    :param regione: (str) regione del fornitore
    :return: restituisce un'istanza del Fornitore se la registrazione ha successo, altrimenti restituisce None
    """
    result, result_message = controlla_campi(nome, cognome, telefono, nome_utente, email, data_di_nascita, piva)
    if not result:
        flash(result_message, "error")
        return False
    else:
        result2, result_message2 = controlla_password(password)
        if not result2:
            flash(result_message2, "error")
            return False
        elif not conferma_password(password, cpassword):
            flash("Le password non corrispondono", "error")
            return False
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

            return True


def registra_admin(nome, cognome, nome_utente, email, password, cpassword, telefono, data_di_nascita, ruolo, regione):
    """
    Registra un amministratore nel sistema
    :param nome:(str) nome dell'amministratore
    :param cognome:(str) cognome dell'amministratore
    :param nome_utente:(str) nome utente dell'amministratore
    :param email:(str) email dell'amministratore
    :param password:(str) password dell'amministratore
    :param cpassword:(str) conferma della password
    :param telefono:(str) numero di telefono dell'amministratore
    :param data_di_nascita: data di nascita dell'amministratore nel formato 'YYYY-MM-DD'
    :param ruolo: (int) ruolo 1 poichè è amministratore
    :param regione: (str) regione dell'amministratore
    :return: Restituisce un'istanza Admin se la registrazione ha successo, altrimenti restituisce None
    """

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


def registra_org(nome, cognome, nome_utente, email, password, cpassword, telefono, data_di_nascita, citta, ruolo,
                 regione):
    """
    Registra un organizzatore nel sistema
    :param nome: (str) nome dell'organizzatore
    :param cognome:(str) cognome dell'organizzatore
    :param nome_utente: (str) nome utente dell'organizzatore
    :param email: (str) email dell'organizzatore
    :param password: (str) password dell'organizzatore
    :param cpassword: (str) conferma della password
    :param telefono:(str) telefono dell'organizzatore
    :param data_di_nascita: (str) data di nascita dell'organizzatore nel formato 'anno-mese-giorno'
    :param citta:(str) città dell'organizzatore
    :param ruolo: (int) ruolo 2 per l'organizzatore
    :param regione:(str) regione dell'organizzatore
    :return:Restituisce un'istanza di Organizzatore se la registrazione ha successo, altrimenti restituisce None
    """

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
                    'Citta': citta
                }
            }

            documento_organizzatore = {**user_data, **organizzatore_data}
            organizzatore = Organizzatore(user_data, organizzatore_data)

            db.Utente.insert_one(documento_organizzatore)

            flash("Registrazione avvenuta con successo!", "success")

            return organizzatore
    return None


def get_dati_area_organizzatore(id_organizzatore):
    """
    Ottiene i dati relativi all'area organizzatore
    :param id_organizzatore: (str) l'id dell'organizzatore di cui si vogliono ottenere i dati
    :return: Una tupla contentente un'itanza di Organizzatore, una lista di EventoPrivato e una lista di Biglietto
    """

    organizzatore_data = db['Utente'].find_one({'_id': ObjectId(id_organizzatore)})
    organizzatore = Organizzatore(organizzatore_data, organizzatore_data)

    eventi_privati_data = list(db['Evento'].find({
        'EventoPrivato.Organizzatore': id_organizzatore,
        'Ruolo': "2"
    }))
    eventi_privati = []
    for data in eventi_privati_data:
        evento_privato = EventoPrivato(data, data)
        eventi_privati.append(evento_privato)

    biglietti_comprati_data = list(db['Biglietto'].find({
        'CompratoDa': id_organizzatore
    }))

    biglietti_comprati = []
    for data in biglietti_comprati_data:
        biglietto = Biglietto(data)
        biglietti_comprati.append(biglietto)

    return organizzatore, eventi_privati, biglietti_comprati


def get_dati_home_organizzatore(id_organizzatore):
    """
    Ottiene i dati per la home page di un organizatore
    :param id_organizzatore: (str) id dell'organizzatore di cui si vogliono ottenere i dati
    :return: Una tupla contenente un'istanza di Evento_privato e una lista di EventoPubblico
    """

    data_odierna = datetime.now().strftime("%d-%m-%Y")

    query = {
        "Ruolo": "2",
        "EventoPrivato.Organizzatore": id_organizzatore,
        "Data": {"$gte": data_odierna},
    }
    try:
        evento_data = db['Evento'].find(query).sort("Data", 1).limit(1).next()
        evento_privato = EventoPrivato(evento_data, evento_data)
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
            evento_pubblico = EventoPubblico(data, data)
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
            evento_pubblico = EventoPubblico(data, data)
            eventi_pubblici.append(evento_pubblico)

    return evento_privato, eventi_pubblici


def get_utente_by_email(email):
    user_data = db.Utente.find_one({'email':email})
    user = Fornitore(user_data, user_data)
    return user
