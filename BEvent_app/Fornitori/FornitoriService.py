from bson import ObjectId
from flask import flash
from ..db import get_db
from ..InterfacciaPersistenza import ServizioOfferto
from ..InterfacciaPersistenza import Organizzatore


def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def validate_servizio_data(descrizione, tipo, prezzo, quantita):
    """
    serve un validare i dati di servizio

    :param descrizione: str
    :param tipo: str
    :param prezzo: float
    :param quantita: int

    :return:false in caso un campo non risetti le condizioni,
    True se invece i campi sono validi

    """
    if len(descrizione) > 500:
        flash("La descrizione non deve superare i 500 caratteri", "error")
        return False

    if tipo not in ['Location', 'Fiorai e Decorazioni', 'Catering', 'Pasticceria', 'Musica e Servizio Audio',
                    'Intrattenimento', 'Animazione per bambini', 'Fotografo', 'Servizi di Trasporto', 'Gadget',
                    'Altro']:
        flash("Il tipo deve essere uno di quelli selezionati", "error")
        return False

    if not is_valid_number(prezzo) or float(prezzo) < 0:
        flash("Il prezzo deve essere un numero non negativo", "error")
        return False
    flash("Aggiunta avvenuto con successo", "succes")
    return True


def get_tutti_servizi_byfornitore(id_fornitore):
    """
    serve a prendere tutti i servizi di uno specifico fornitore grazie al suo  id

    :param id_fornitore: (str) id del fornitore

    :return: lista dei servizi del fornitore con un dato id
    """
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    servizi_data = list(servizi_collection.find(
        {'fornitore_associato': id_fornitore, 'isCurrentVersion': {'$in': [None, '']}, 'isDeleted': False}))

    lista_servizi = []

    for data in servizi_data:
        servizio = ServizioOfferto.ServizioOfferto(data)
        lista_servizi.append(servizio)

    return lista_servizi


def get_dati_fornitore(id_fornitore):
    """
    serve a ricavare tutti i dati di uno specifico fornitore grazie al suo id

    :param id_fornitore: (str) id del fornitore

    :return: lista dei dati del fornitore
    """
    from ..InterfacciaPersistenza.Fornitore import Fornitore
    db = get_db()
    user_data = db['Utente'].find_one({"_id": ObjectId(id_fornitore)})
    fornitore = Fornitore(user_data, user_data)
    return fornitore


def aggiorna_foto_fornitore(id_fornitore, byte_arrays_bytes):
    """
    serve ad aggiornare le foto di un dato fornitore
    :param id_fornitore: (str) id del fornitore
    :param byte_arrays_bytes: (byte_array) Array di byte che rappresentano le foto di un fornitore
    :return: messaggio di successo in caso di riuscito inseromento al contrario messaggio di errore
    """
    db = get_db()
    collection = db['Utente']
    try:

        result = collection.update_one(
            {"_id": ObjectId(id_fornitore)},
            {"$push": {"Fornitore.Foto": {"$each": byte_arrays_bytes}}}
        )
        if result.modified_count > 0:
            return "Foto aggiornata con successo"
        else:
            return "Nessun documento aggiornato"
    except Exception as e:
        return f"Si è verificato un errore: {e}"


def elimina_servizio(servizio_id):
    """
    serve ad eliminare un servizio dato il suo id, se il servizio non è stato prenotato e successivamente pagato elimina
    del tutto il servizio dal database, altrimenti imposta a true il campo "isDeleated"

    :param servizio_id: (str) id del servizio offerto

    :return:
    """
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    eventi_collection = db['Evento']

    evento_associato = eventi_collection.find_one({
        "servizi_associati": servizio_id,
        "isPagato": True
    })
    if evento_associato:
        result = servizi_collection.update_one(
            {"_id": ObjectId(servizio_id)},
            {"$set": {"isDeleted": True}}
        )
        return result
    else:
        servizi_collection.delete_one({"_id": ObjectId(servizio_id)})


def modifica_servizio(nuovi_dati, servizio_id):
    """
    serve a modificare un servizio offerto, se quest'ultimo è stato già prenotato in un evento crea un nuovo servizio offerto
    con i campi modificati mentre il servizio con quell'id già esistente cambierà il campo "isCurrentVersion" con l'id del servizio appena creato.
    se quest'ultimo non è
    :param nuovi_dati: (dict) dizionario con tutti  i dati relativi al servizio

    :return: restituisce l'id del servizio modificato
    """
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    eventi_collection = db['Evento']

    evento_associato = eventi_collection.find_one({
        "servizi_associati": servizio_id,
        "isPagato": True
    })

    if evento_associato:

        servizio_corrente = servizi_collection.find_one({"_id": ObjectId(servizio_id)})

        if servizio_corrente:

            servizio_modificato = servizio_corrente.copy()
            campi_da_modificare = {k: v for k, v in nuovi_dati.items() if v is not None}
            servizio_modificato.update(campi_da_modificare)

            servizio_modificato.pop('_id', None)

            result = servizi_collection.insert_one(servizio_modificato)

            nuovo_servizio_id = result.inserted_id

            servizi_collection.update_one(
                {"_id": ObjectId(servizio_id)},
                {"$set": {"isCurrentVersion": nuovo_servizio_id}}
            )

            return nuovo_servizio_id

    else:

        servizio_corrente = servizi_collection.find_one({"_id": ObjectId(servizio_id)})

        if servizio_corrente:
            campi_da_modificare = {k: v for k, v in nuovi_dati.items() if v is not None}
            servizi_collection.update_one(
                {"_id": ObjectId(servizio_id)},
                {"$set": campi_da_modificare}
            )

            return servizio_id

    return None


def aggiungi_servizio(nuovi_dati):
    """
    Aggiunge al database un servizio se quest'ultimo è valido
    :param nuovi_dati: (dict) dizionario con tutti  i dati relativi al servizio
    :return: True se il servizio è stato inserito, false se quest'ultimo non è stato inserito
    """
    result = validate_servizio_data(nuovi_dati['Descrizione'], nuovi_dati['Tipo'], nuovi_dati['Prezzo'], 2)
    if result:
        db = get_db()
        db['Servizio Offerto'].insert_one(nuovi_dati)
        return True
    else:
        return False


def get_eventi_by_fornitore_privato(id):
    """
    serve ad ottenere la tutti gli eventi privati nei quali un fornitore ha un suo servizio prenotato
    :param id: (str) id del fornitore
    :return: la lista degli eventi
    """
    from ..InterfacciaPersistenza import EventoPrivato
    print(id)
    db = get_db()
    eventi = db['Evento']
    eventi_fornitore_privati = eventi.find({"fornitori_associati": id, "Ruolo": "2"})

    lista_eventi_fornitore = []
    for evento_fornitore in eventi_fornitore_privati:
        evento_privato = EventoPrivato.EventoPrivato(evento_fornitore, evento_fornitore)
        lista_eventi_fornitore.append(evento_privato)

    return lista_eventi_fornitore


def get_eventi_fornitore_pubblico(id):
    """
     serve ad ottenere la tutti gli eventi pubblici nei quali un fornitore ha un suo servizio prenotato
    :param id: (str) id del fornitore
    :return: la lista degli eventi
    """
    from ..InterfacciaPersistenza import EventoPubblico
    print(id)
    db = get_db()
    eventi = db['Evento']
    eventi_fornitore_pubblico = eventi.find({"fornitori_associati": id, "Ruolo": "1"})

    lista_eventi_fornitore = []
    for evento_fornitore in eventi_fornitore_pubblico:
        evento_pubblico = EventoPubblico.EventoPubblico(evento_fornitore, evento_fornitore)
        lista_eventi_fornitore.append(evento_pubblico)

    return lista_eventi_fornitore


def cancella_evento(id):
    """
    Cancella un evento Pubblico in base all'id dell'evento
    :param id: (str) id dell'evento
    """
    db = get_db()
    eventi = db['Evento']
    eventi.delete_one({"_id": ObjectId(id)})


def get_dettagli_evento(id):
    """
    serve a vedere tutti i dettagli relativi ad un evento privato
    :param id: (str) id dell'evento
    :return: evento cercato
    """
    from ..InterfacciaPersistenza import EventoPrivato
    db = get_db()
    eventi = db['Evento']
    evento_data = eventi.find_one({"_id": ObjectId(id),
                                   "Ruolo": "2"})
    if evento_data:
        evento = EventoPrivato.EventoPrivato(evento_data, evento_data)
        flash("nessun dettaglio", category="success")
    else:
        evento = None
        flash("ok", "warning")
    return evento


def get_dati_organizzatore(id):
    """
     serve a vedere tutti i dettagli relativi ad un organizzatore tramite l'id di un evento
    :param id: (str) id dell'evento
    :return: organizzatore ricercato
    """
    from ..InterfacciaPersistenza import EventoPrivato
    db = get_db()
    eventi = db['Evento']
    evento_data = eventi.find_one({"_id": ObjectId(id)})
    evento = EventoPrivato.EventoPrivato(evento_data, evento_data)
    utenti = db['Utente']
    utenti_data = utenti.find_one({"_id": ObjectId(evento.organizzatore)})
    organizzatore = Organizzatore.Organizzatore(utenti_data, utenti_data)
    return organizzatore


def get_dati_servizi(id, id_fornitore):
    """
    serve a vedere tutti i dettagli dei servizi offerti impiegati in un determinato evento escludendo i servizi di un fornitore( ovvero quello
    che ha richiesto questa funzione)
    :param id: (str) id dell'evento
    :param id_fornitore: (str) id del fornitore da escludere dalla ricerca
    :return: organizzatore ricercato
    """
    from ..InterfacciaPersistenza import EventoPrivato
    db = get_db()
    eventi = db['Evento']

    evento_data = eventi.find_one({"_id": ObjectId(id)})
    evento = EventoPrivato.EventoPrivato(evento_data, evento_data)
    servizi_lista = []
    for servizi in evento.servizi_associati:
        servizio_data = db['Servizio Offerto'].find_one({"_id": ObjectId(servizi)})

        if not (servizio_data and ObjectId(servizio_data["fornitore_associato"]) == ObjectId(id_fornitore)):
            servizi_lista.append(servizio_data)

    return servizi_lista


def invio_feed_back(id_valutato, id_valutante, valutazione):
    """
    Funzione che permette di lasciare un feedback
    :param id_valutato: (str) id del servizio valutato
    :param id_valutante: (str) id del fornitore che sta lasciando il feedback
    :param valutazione:(str) valutazione del servizio

    """
    db = get_db()
    dati = {
        "id_valutato": id_valutato,
        "id_valutante": id_valutante,
        "valutazione": valutazione
    }
    db['FeedBack'].insert_one(dati)


def get_fornitori(id_fornitori):
    """
    
    """
    from ..InterfacciaPersistenza.Fornitore import Fornitore
    db = get_db()
    lista_id = [ObjectId(id_str) for id_str in id_fornitori]
    risultati = db['Utente'].find({'_id': {'$in': lista_id}})

    lista_fornitori = []
    for user_data in risultati:
        lista_fornitori.append(Fornitore(user_data, user_data))

    return lista_fornitori

def sponsorizza(id):
    db =get_db()
    Eventi = db['Evento']
    Eventi.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"isPagato": True}}
    )