from datetime import datetime
from bson import ObjectId
from flask import flash
import re
from ..InterfacciaPersistenza import ServizioOfferto
from ..InterfacciaPersistenza.EventoPrivato import EventoPrivato
from ..db import get_db
from ..InterfacciaPersistenza.Fornitore import Fornitore
from ..InterfacciaPersistenza.ServizioOfferto import ServizioOfferto

db = get_db()


def is_valid_data(data):
    """
    Funzione per verificare che la data inserita sia valida. Viene quindi controllato che la data sia > alla data
    odierna.

    :param data: (str) data inserita dall'utente nella pagina SceltaEventoDaCreare.html

    :return: True se la data è corretta, False altrimenti
    """
    date_format_regex = re.compile(r'^\d{2}-\d{2}-\d{4}$')

    if not date_format_regex.match(data):
        return False, "Formato data non corretto. Utilizzare il formato dd-mm-yyyy."

    try:
        datetime_data = datetime.strptime(data, '%d-%m-%Y')

        data_odierna = datetime.now()

        if datetime_data > data_odierna:
            return True, "La data è corretta nel formato ed è anche valida."
        else:
            return False, "La data non è valida poichè è precedente alla data odierna."

    except ValueError:
        return False, "Errore nella conversione della data."


def get_fornitori_disponibli(data_richiesta):
    """
    Funzione che ottiene tutti i fornitori che sono disponibili in una determinata data, prendendola dal database.
    Usa una pipeline per verificare quali sono disponibili.

    :param data_richiesta: (str) stringa che indica la data in cui si vuole creare un evento
    :return: lista di oggetti di tipo Fornitore, ovvero i fornitori disponibli
    """

    pipeline = [
        {"$match": {"Ruolo": "3"}},
        {
            "$lookup": {
                "from": "Evento",
                "let": {"fornitore_id_str": {"$toString": "$_id"}},
                "pipeline": [
                    {
                        "$unwind": "$Evento.fornitori_associati"
                    },
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$$fornitore_id_str", "$Evento.fornitori_associati"]},
                                    {"$eq": ["$Evento.Data", data_richiesta]},
                                    {"$eq": ["$Evento.isPagato", True]}
                                ]
                            }
                        }
                    }
                ],
                "as": "eventi_associati"
            }
        },
        {
            "$addFields": {
                "eventiPrenotati": {"$size": "$eventi_associati"},
                "EventiMassimiGiornaliero": "$Fornitore.EventiMassimiGiornaliero"
            }
        },
        {
            "$match": {
                "$expr": {"$lt": ["$eventiPrenotati", "$EventiMassimiGiornaliero"]}
            }
        }
    ]

    fornitori_disponibili = list(db.Utente.aggregate(pipeline))
    lista_fornitori = []

    for data in fornitori_disponibili:
        fornitore = Fornitore(data, data)
        lista_fornitori.append(fornitore)

    return lista_fornitori


def get_servizi(data_richiesta):
    """
    Funzione che ottiene dal database tutti i servizi che si possono prenotare in una determinata data, poichè alcuni
    potrebbero essere impegnati in un evento.
    -Vengono prese dal databse le collezioni Servizio Offerto e Evento
    -Viene controllata la versione dei servizi in modo da prendere i servizi la cui versione corrisponde all'ultima
    rilasciata dal fornitore
    -Usando la lista di servizi precedentemente filtrati, essi vengono nuovamente filtrati per prendere solo i servizi
    che non sono prenotati in un evento nella data inserita dall'organizzatore.

    :param data_richiesta: (str) stringa che indica la data in cui si vuole creare un evento

    :return: lista di oggetti di tipo Servizio Offerto, ovvero i servizi disponibli
    """

    servizi_collection = db['Servizio Offerto']
    eventi_collection = db['Evento']

    servizi_data = list(
        servizi_collection.find({'$or': [{'isCurrentVersion': None}, {'isCurrentVersion': {'$exists': False}}]}))

    lista_servizi = []

    for data in servizi_data:
        servizio = ServizioOfferto(data)
        evento_associato = eventi_collection.find_one({
            'servizi_associati': {'$in': [str(servizio._id)]},
            'Data': data_richiesta,
            '$or': [
                {'Ruolo': '2', 'isPagato': True},
                {'Ruolo': '1'}
            ]
        })

        if not evento_associato:
            lista_servizi.append(servizio)

    return lista_servizi


def filtro_categoria_liste(categoria, data):
    """
    Funzione per ottenere dal database la lista di fornitori e servizi che appartengono alla categoria inserita
    dall'utente. -Vengono prese le liste di fornitori e servizi disponibli nella data indicata dall'organizzatore.
    -La lista dei servizi viene filtrata per prendere i servizi che hanno il parametro "tipo" che corrisponde alla
    categoria indicata dall'organizzatore. -In base ai servizi filtrati viene filtrata la lista dei fornitori per
    ottenere i fornitori ai quali appartengono i servizi selezionati.

    :param categoria: (str) stringa che indica la categoria di servizio che si vuole filtrare
    :param data: (str) stringa che indica la data nella quale si vuole fare l'evento

    :return: due liste filtrate di oggetti: servizi filtrati (lista di oggetti di tipo Servizio Offerto) e fornitori
    filtrati (lista di oggetti di tipo Fornitore)
    """
    servizi = get_servizi(data)
    fornitori_non_filtrati = get_fornitori_disponibli(data)
    servizi_non_filtrati = filtrare_servizi_per_fornitore(servizi, fornitori_non_filtrati)

    servizi_filtrati = [servizio for servizio in servizi_non_filtrati if servizio.tipo == categoria]

    id_fornitori = set(servizio.fornitore_associato for servizio in servizi_filtrati)

    fornitori_filtrati = [fornitore for fornitore in fornitori_non_filtrati if fornitore.id in id_fornitori]

    return servizi_filtrati, fornitori_filtrati


def filtro_regione_liste(regione, data):
    """
    Funzione per ottenere dal database la lista di fornitori e servizi che si trovano nella regione inserita dall'
    organizzatore.
    -Vengono prese le liste di fornitori e servizi disponibli nella data indicata dall'organizzatore.
    -La lista dei fornitori viene filtrata per prendere i fornitori che hanno il parametro "regione" che corrisponde
    alla regione indicata dall'organizzatore.
    -In base alla lista di fornitori selezionati vengono presi i servizi associati.

    :param regione: (str) stringa che indica la regione a cui devono appartenere i fornitori
    :param data: (str) stringa che indica la data nella quale si vuole fare l'evento

    :return: due liste filtrate di oggetti: servizi_filtrati (lista di oggetti di tipo Servizio Offerto) e
    fornitori_filtrati (lista di oggetti di tipo Fornitore)

    """
    servizi = get_servizi(data)
    fornitori_non_filtrati = get_fornitori_disponibli(data)

    fornitori_filtrati = [fornitore for fornitore in fornitori_non_filtrati if fornitore.regione == regione]

    servizi_filtrati = filtrare_servizi_per_fornitore(servizi, fornitori_filtrati)

    return servizi_filtrati, fornitori_filtrati


def filtro_prezzo_liste(prezzo_min, prezzo_max, data):
    """
    Funzione per ottenere dal database la lista di fornitori e servizi il cui prezzo si trova nel range di prezzo
    inserito dall'organizzatore.
    -Vengono prese le liste di fornitori e servizi disponibli nella data indicata dall'organizzatore.
    -La lista dei servizi viene filtrata per prendere i servizi che rientrano nel range di prezzi indicati dall'
    organizzatore.
    -In base alla lista di servizi selezionati vengono presi i fornitori associati.

    :param prezzo_min: (str) stringa che indica il prezzo minimo del range di prezzo scelto dall'organizzatore
    :param prezzo_max: (str) stringa che indica il prezzo massimo del range di prezzo scelto dall'organizzatore
    :param data: (str) stringa che indica la data nella quale si vuole fare l'evento

    :return: due liste filtrate di oggetti: servizi_filtrati (lista di oggetti di tipo Servizio Offerto) e
    fornitori_filtrati (lista di oggetti di tipo Fornitore)

   """

    servizi = get_servizi(data)
    fornitori_non_filtrati = get_fornitori_disponibli(data)
    servizi_non_filtrati = filtrare_servizi_per_fornitore(servizi, fornitori_non_filtrati)

    if prezzo_min == "" and prezzo_max == "":
        return servizi_non_filtrati, fornitori_non_filtrati
    elif prezzo_min == "" and float(prezzo_max) >= 0:
        servizi_filtrati = [servizio for servizio in servizi_non_filtrati if float(servizio.prezzo) <=
                            float(prezzo_max)]
    elif float(prezzo_min) >= 0 and prezzo_max == "":
        servizi_filtrati = [servizio for servizio in servizi_non_filtrati if
                            float(prezzo_min) <= float(servizio.prezzo)]
    else:
        servizi_filtrati = [servizio for servizio in servizi_non_filtrati if
                            float(prezzo_min) <= float(servizio.prezzo) <= float(prezzo_max)]

    id_fornitori = set(servizio.fornitore_associato for servizio in servizi_filtrati)
    fornitori_filtrati = [fornitore for fornitore in fornitori_non_filtrati if fornitore.id in id_fornitori]

    return servizi_filtrati, fornitori_filtrati


def filtrare_servizi_per_fornitore(servizi_non_filtrati, fornitori_filtrati):
    """
    Funzione che restituisce la lista di servizi filtrata in base ai fornitori precedentemente filtrati. Per farlo viene
    usata una lista di id dei fornitori passati come argomento.

    :param servizi_non_filtrati: lista di oggetti di tipo servizio offerto non filtrati in base al fornitore
    :param fornitori_filtrati: lista di oggetti di tipo fornitore che serve a filtrare la lista di servizi
    corrispondenti

    :return: una lista servizi_filtrati (lista di oggetti di tipo Servizio Offerto)

    """
    id_fornitori = set(fornitore.id for fornitore in fornitori_filtrati)

    servizi_filtrati = [servizio for servizio in servizi_non_filtrati if
                        servizio.fornitore_associato in id_fornitori]
    return servizi_filtrati


def filtro_ricerca(ricerca, data):
    """
    Funzione per ottenere dal database la lista di fornitori e servizi la cui descrizione o nome contiene la parola
    inserita dall'organizzatore.
    -Vengono prese le liste di fornitori e servizi disponibli nella data indicata dall'organizzatore.
    -Vengono filtrati i fornitori cercando la parola sia nel nome che nella descrizione
    -In base alla lista di fornitori selezionati vengono presi i servizi associati.

    :param ricerca: (str) stringa che indica la parola da ricercare scelta dall'organizzatore
    :param data: (str) stringa che indica la data nella quale si vuole fare l'evento

    :return: due liste filtrate di oggetti: servizi_filtrati (lista di oggetti di tipo Servizio Offerto) e
    fornitori_filtrati (lista di oggetti di tipo Fornitore)

   """
    servizi = get_servizi(data)
    fornitori_non_filtrati = get_fornitori_disponibli(data)
    servizi_non_filtrati = filtrare_servizi_per_fornitore(servizi, fornitori_non_filtrati)

    fornitori_filtrati_nome = [fornitore for fornitore in fornitori_non_filtrati if
                               ricerca.lower() in fornitore.nome_utente.lower()
                               ]

    fornitori_filtrati_desctizione = [fornitore for fornitore in fornitori_non_filtrati if ricerca.lower() in
                                      fornitore.descrizione.lower()]

    fornitori_filtrati = None
    if fornitori_filtrati_desctizione and fornitori_filtrati_nome:
        fornitori_unici = {}

        for fornitore in fornitori_filtrati_nome + fornitori_filtrati_desctizione:
            fornitori_unici[fornitore.id] = fornitore

        fornitori_filtrati = list(fornitori_unici.values())
    elif fornitori_filtrati_desctizione:
        fornitori_filtrati = fornitori_filtrati_desctizione
    elif fornitori_filtrati_nome:
        fornitori_filtrati = fornitori_filtrati_nome

    if fornitori_filtrati:
        servizi_filtrati = filtrare_servizi_per_fornitore(servizi_non_filtrati, fornitori_filtrati)
    else:
        servizi_filtrati = None

    return servizi_filtrati, fornitori_filtrati


def get_fornitore_by_email(email):
    """
    Funzione per ottenere dal database i dati del fornitore in base alla sua email

    :param email: (str) stringa che contiene l'email del fornitore che si vuole cercare

    :return: oggetto Fornitore, che rappresenta il fornitore trovato nel database

    """

    fornitore_data = db['Utente'].find_one({"email": email})
    fornitore = Fornitore(fornitore_data, fornitore_data)
    return fornitore


def get_servizi_fornitore(fornitore, datarichiesta):
    """
    Funzione per ottenere dal database i servizi corrispondenti a un singolo fornitore. Vengono prima presi tutti i
    servizi disponibili in una data scelta e poi vengono filtrati per ottenere solo quelli associati al fornitore
    indicato.

    :param fornitore: (obj) oggetto della classe Fornitore che contiene i dati del fornitore scelto
    :param datarichiesta: (str)  stringa che indica la data nella quale si vuole fare l'evento

    :return: lista_servizi, ovvero una lista di oggetti di tipo Servizio Offerto
    """
    servizi_non_filtrati = get_servizi(datarichiesta)

    lista_servizi = [servizio for servizio in servizi_non_filtrati if servizio.fornitore_associato == fornitore.id]

    return lista_servizi


def fornitore_serializer(fornitore):
    """
    Funzione per serializzare un oggetto della classe fornitore in modo che sia passabile come risposta json.

    :param fornitore: (obj) oggetto della classe Fornitore che contiene i dati del fornitore scelto

    :return: dizionario che rappresenta i dati dell'oggetto fornitore
    """
    return {
        "id": fornitore.id,
        "nome": fornitore.nome,
        "foto": fornitore.foto,
        "citta": fornitore.citta,
        "regione": fornitore.regione,
        "OrarioDiLavoro": fornitore.orario_lavoro,
        "email": fornitore.email,
        "nome_utente": fornitore.nome_utente,
        "descrizione": fornitore.descrizione
    }


def servizio_serializer(servizio):
    """
    Funzione per serializzare un oggetto della classe servizio in modo che sia passabile come risposta json.

    :param servizio: (obj) oggetto della classe Servizio Offerto che contiene i dati del servizio scelto

    :return: dizionario che rappresenta i dati dell'oggetto servizio
    """
    return {
        "id": servizio._id,
        "tipo": servizio.tipo,
        "fornitore_associato": servizio.fornitore_associato,
        "descrizione": servizio.descrizione,
        "prezzo": servizio.prezzo,
        "foto_servizio": servizio.foto_servizio
    }


def get_servizio_by_id(id_servizio):
    """
    Funzione per ottenere dal database i dati di un singolo servizio in base al suo id

    :param id_servizio: (str) stringa che rappresenta l'id del servizio scelto

    :return: oggetto di tipo servizio Offerto
    """

    id_servizio_obj = ObjectId(id_servizio)
    servizio_data = db["Servizio Offerto"].find_one({"_id": id_servizio_obj})
    servizio = ServizioOfferto(servizio_data)
    return servizio


def get_fornitore_by_id(id_fornitore):
    """
    Funzione per ottenere dal database i dati di un singolo fornitore in base al suo id

    :param id_fornitore: (str) stringa che rappresenta l'id del fornitore scelto

    :return: oggetto di tipo fornitore
    """
    id_fornitore_obj = ObjectId(id_fornitore)
    fornitore_data = db['Utente'].find_one({"_id": id_fornitore_obj})
    fornitore = Fornitore(fornitore_data, fornitore_data)
    return fornitore


def ottieni_servizi_e_fornitori_cookie(carrello):
    """
    Funzione per ottenere la lista dei fornitori e dei servizi in base a ciò che è stato salvato nei cookie.

    :param carrello: (str) stringa che rappresenta i cookie del carrello

    :return: due liste di oggetti: lista_servizi (lista di oggetti di tipo servizio Offerto) e lista_fornitori (lista di
    oggetti di tipo Fornitore)
    """
    lista_servizi = []

    for id_servizio in carrello:
        if id_servizio != '' and id_servizio is not None:
            servizio = get_servizio_by_id(id_servizio)
            lista_servizi.append(servizio)

    lista_fornitori = []
    if lista_servizi:
        for servizio in lista_servizi:
            fornitore = get_fornitore_by_id(servizio.fornitore_associato)
            if fornitore not in lista_fornitori:
                lista_fornitori.append(fornitore)

    return lista_servizi, lista_fornitori


def crea_documento_evento_generico(data_evento, descrizione, tipo_evento, n_invitati, foto_byte_array, ruolo,
                                   id_fornitori, id_servizi, is_pagato):
    """
    Funzione per creare il documento da inserire nel database che contiene gli attributi dell'evento comuni sia all'
    evento privato che all'evento pubblico

    :param data_evento: (str) stringa che rappresenta la data in cui si terrà l'evento
    :param descrizione: (str) stringa che rappresenta la descrzione dell'evento
    :param tipo_evento: (str) stringa che rappresenta il tipo di evento
    :param n_invitati: (str) stringa che rappresenta il numero di persone invitate o i posti disponibli
    :param foto_byte_array: (byte_array) byte array che rappresenta l'immagine locandina dell'evento
    :param ruolo: (str) indica se l'evento è di tipo privato ("2") o pubblico ("3")
    :param id_fornitori: (array) array che continene l'id dei fornitori coinvolti nell'evento
    :param id_servizi: (array) array che continene l'id dei servizi coinvolti nell'evento
    :param is_pagato: (bool) indica se l'evento è stato pagato

    :return: documento da inserire nel database

    """
    documento = {
        '_id': ObjectId(),
        'Data': data_evento,
        'Descrizione': descrizione,
        'Tipo': tipo_evento,
        'Invitati/Posti': n_invitati,
        'Locandina': foto_byte_array,
        'Ruolo': ruolo,
        'fornitori_associati': id_fornitori,
        'servizi_associati': id_servizi,
        'isPagato': is_pagato
    }

    return documento


def save_evento(lista_servizi, lista_fornitori, tipo_evento, data_evento, n_invitati, nome_festeggiato, descrizione,
                is_pagato, ruolo, foto_byte_array, prezzo, id_organizzatore):
    """
    Funzione per salvare l'evento privato nel database che crea il documento da inserire mettendo come valore dei campi
    i dati passati come parametri.

    :param    lista_servizi:(list) lista di oggetti servizio offerto
    :param    lista_fornitori: (list) lista di oggetti fornitore
    :param    tipo_evento: (str) stringa che rappresenta il tipo di evento che si sta creando
    :param    data_evento: (str) stringa che rappresenta la data nella quale si svolgerà l'evento
    :param    n_invitati: (str) stringa che rappresenta il numero di invitati previsti
    :param    nome_festeggiato: (str) stringa che rappresenta il nome del festeggiato
    :param    descrizione: (str) stringa che rappresenta una descrizione dell'evento
    :param    is_pagato: (bool) booleano che indica se l'evento è stato pagato o meno
    :param    ruolo: (str) stringa che indica se l'evento è pubblico o privato
    :param    foto_byte_array: (byte_array) byte array che rappresenta una foto dell'evento
    :param    prezzo: (str) stringa che rappresenta il prezzo totale dell'evento
    :param    id_organizzatore: (str) stringa che rappresenta l'id dell'organizzatore

    :return: l'evento privato inserito nel database
    """
    if not isinstance(tipo_evento, str) or not re.match(r'^[^0-9]*$', tipo_evento):
        flash("Il tipo di evento non rispetta il formato previsto", "error")
        return False
    else:
        result, result_message = is_valid_data(data_evento)
        if not result:
            flash(result_message, "error")
            return False
        elif not isinstance(n_invitati, str) or not re.match(r'^(?!0$)[0-9]+$', n_invitati):
            flash("Il numero di invitati non rispetta il formato previsto", "error")
            return False
        else:
            id_fornitori = [fornitore.id for fornitore in lista_fornitori]
            id_servizi = [servizio._id for servizio in lista_servizi]
            documento_evento_generico = crea_documento_evento_generico(data_evento, descrizione, tipo_evento,
                                                                       n_invitati,
                                                                       foto_byte_array, ruolo, id_fornitori, id_servizi,
                                                                       is_pagato)
            documento_evento_privato = {
                'EventoPrivato': {
                    'Prezzo': prezzo,
                    'Festeggiato/i': nome_festeggiato,
                    'Organizzatore': id_organizzatore
                }
            }

            documento_evento = {**documento_evento_generico, **documento_evento_privato}
            db.Evento.insert_one(documento_evento)
            flash("L'evento è stato creato correttamente", "success")
            return True


def elimina_evento(id_evento):
    """
    Funzione per eliminare un evento dal databse in base all'id dell'evento fornito

    :param id_evento: (str) id dell'evento che si vuole cancellare

    :return: true per indicare che l'evento è stato cancellato
    """
    evento = db.Evento.find_one({"_id": ObjectId(id_evento)})

    evento_privato = EventoPrivato(evento, evento)
    if evento_privato is None:
        return False, "Evento non trovato"

    if evento_privato:
        evento_privato.notify_observers()

        # Eliminazione dell'evento
    db.Evento.delete_one({"_id": ObjectId(id_evento)})

    return True, "Evento eliminato e fornitori notificati"


def crea_evento_pubblico(data, n_persone, descrizione, locandina, ruolo, tipo, is_pagato, fornitori_associati,
                         servizi_associati, prezzo, ora, nome, via, regione):
    """
    Funzione per salvare l'evento pubblico nel database che crea il documento da inserire mettendo come valore dei campi
    i dati passati come parametri.

    :param data: (str) stringa che rappresenta la data nella quale si terrà l'evento
    :param n_persone: (str) stringa che rappresenta il numero di posti disponibili
    :param descrizione: (str) stringa che rappresenta una descrizione dell'evento
    :param locandina: (byte_array) byte array che rappresenta una foto dell'evento
    :param ruolo: (str) stringa che rappresenta il ruolo dell'evento se pubblico o privato
    :param tipo: (str) stringa che rappresenta il tipo di evento pubblico
    :param is_pagato: (bool) booleano che indica se l'evento è stato pagato per la sponsorizzazione o meno
    :param fornitori_associati: (list) lista di oggetti fornitore
    :param servizi_associati: (list) lista di oggetti servizio offerto
    :param prezzo: (str) stringa che rappresenta il prezzo di un biglietto per partecipare all'evento
    :param ora: (str) stringa che rappresenta l'ora in cui si terrà l'evento
    :param nome: (str) stringa che rappresenta il nome dell'evento
    :param via: (str) stringa che rappresenta il luogo dove si terrà l'evento
    :param regione: (str) stringa che rappresenta la regione dove si terrà l'evento

    :return: nulla
    """

    if not valid_evento(data, n_persone, tipo, prezzo, ora):
        return False

    documento_evento_generico = crea_documento_evento_generico(data, descrizione, tipo, n_persone,
                                                               locandina, ruolo, fornitori_associati, servizi_associati,
                                                               is_pagato)

    documento_evento_pubblico = {
        'EventoPubblico': {
            'Prezzo': prezzo,
            'Nome': nome,
            'Luogo': via,
            'Regione': regione,
            'Ora': ora,
            'BigliettiDisponibili': n_persone
        }
    }
    documento_evento = {**documento_evento_generico, **documento_evento_pubblico}
    db.Evento.insert_one(documento_evento)
    return True


def valid_evento(data, n_persone, tipo, prezzo, ora):
    result, result_message = is_valid_data(data)
    if not result:
        flash(result_message, "error")
        return False

    if not isinstance(n_persone, str):
        flash('il numero di persone deve essere maggiore di 0', "error")
        return False

    if tipo not in ['Conferenze e Seminari', 'Concerti e Spettacoli', 'Mostre ed Esposizioni', 'Corsi e Workshop',
                    'Eventi Benefici', 'Eventi Sociali']:
        flash('il tipo deve essere uno di quelli selezionati', "error")
        return False

    if not isinstance(prezzo, str) or not re.match(r'^(?!0$)[0-9]+$', prezzo):
        flash('il prezzo selezionato non è valido', "error")
        return False

    pattern = re.compile(r'^[0-2][0-9]:[0-5][0-9]$')
    if not bool(re.match(pattern, ora)):
        flash('l ora non  rispetta il formato', "error")
        return False

    flash('tutti i campi sono stati compilati correttamente', "succes")
    return True


def get_tutti_servizi_by_fornitore_location(id_fornitore):
    """
    Funzione che prende i servizi di tipo location associati ad un fornitore

    :param id_fornitore: (str) id del fornitore scelto

    :return : lista_servizi, ovvero una lista di oggetti di tipo servizio offerto

    """
    servizi_collection = db['Servizio Offerto']
    servizi_data = servizi_collection.find({
        'fornitore_associato': id_fornitore,
        'isCurrentVersion': {'$in': [None, '']},
        'isDeleted': False,
        'Tipo': 'Location'
    })
    lista_servizi = []

    for data in servizi_data:
        servizio = ServizioOfferto(data)
        lista_servizi.append(servizio)

    return lista_servizi


def acquista_biglietto(id_evento, id_organizzatore, numero_biglietti):
    """
    Funzione per acquistare un biglietto e salvarlo nel database. Per salvarlo recupera delle informazioni utili dalla
    collezione evento. Inoltre modifica la variabile biglietti disponibili nel documento dell'evento a cui
    corrispondono i biglietti

    :param id_evento: (str) stringa che rappresenta l'id dell'evento
    :param id_organizzatore: (str) stringa che reppresenta l'id dell'organizzatore
    :param numero_biglietti: (str) stringa che indica il numero di biglietti che si vogliono acquistare
    :return: nulla
    """
    from ..InterfacciaPersistenza import EventoPubblico
    eventi = db['Evento']
    biglietti = db["Biglietto"]
    evento_data = eventi.find_one({"_id": ObjectId(id_evento)})
    evento = EventoPubblico.EventoPubblico(evento_data, evento_data)

    biglietto_data = {
        "Evento_associato": id_evento,
        "CompratoDa": id_organizzatore,
        "DataEvento": evento.data,
        "Dove": evento.luogo,
        "Ora": evento.ora,
        "Quantità": numero_biglietti,
        'NomeEvento': evento.nome
    }
    biglietto = int(evento.biglietti_disponibili)
    numero = int(numero_biglietti)
    nuovo_num_biglietti = biglietto - numero
    nuovo_num_biglietti = str(nuovo_num_biglietti)

    biglietti.insert_one(biglietto_data)

    eventi.update_one(
        {"_id": ObjectId(id_evento)},
        {"$set": {"EventoPubblico.BigliettiDisponibili": nuovo_num_biglietti}}
    )


def get_dati_servizi_organizzatore(id_evento):
    """
    Funzione che prende dal database i servizi coinvolti nell'evento dell'organizzatore

    :param id_evento: (str) stringa che rappresenta l'id dell'evento

    :return: servizi_lista (lista di oggetti di tipo Servizio Offerto)
    """
    from ..InterfacciaPersistenza import EventoPrivato
    eventi = db['Evento']
    evento_data = eventi.find_one({"_id": ObjectId(id_evento)})
    evento = EventoPrivato.EventoPrivato(evento_data, evento_data)
    servizi_lista = []
    for servizi in evento.servizi_associati:
        servizio_data = db['Servizio Offerto'].find_one({"_id": ObjectId(servizi)})
        servizi_lista.append(servizio_data)
    return servizi_lista
