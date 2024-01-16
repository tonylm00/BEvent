from bson import ObjectId
from pymongo import MongoClient


from ..db import get_db
from ..InterfacciaPersistenza import ServizioOfferto
from ..InterfacciaPersistenza import Evento
from ..InterfacciaPersistenza import Organizzatore




def get_tutti_servizi_byFornitore(id_fornitore):
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    servizi_data = list(servizi_collection.find(
        {'fornitore_associato': id_fornitore, 'isCurrentVersion': {'$in': [None, '']}, 'isDeleted': False}))

    lista_servizi = []

    for data in servizi_data:
        servizio = ServizioOfferto.Servizio_Offerto(data)
        lista_servizi.append(servizio)

    return lista_servizi


def get_dati_fornitore(id_fornitore):
    from ..InterfacciaPersistenza.Fornitore import Fornitore
    db = get_db()
    user_data = db['Utente'].find_one({"_id": ObjectId(id_fornitore)})
    fornitore = Fornitore(user_data, user_data)
    return fornitore


def aggiorna_foto_fornitore(id_fornitore, byte_arrays_bytes):
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
    print("ci sono qui sto per eliminare attenti")
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    eventi_collection = db['Evento']

    # Verifica se il servizio è presente in almeno un evento associato a un determinato fornitore
    evento_associato = eventi_collection.find_one({
        "servizi_associati": servizio_id,
        "isPagato": True
    })
    print(evento_associato)
    if evento_associato:
        print("ci sono")
        result = servizi_collection.update_one(
            {"_id": ObjectId(servizio_id)},
            {"$set": {"isDeleted": True}}
        )
        return result
    else:
        print("ci sono 2")
        servizi_collection.delete_one({"_id": ObjectId(servizio_id)})


def modifica_servizio(nuovi_dati, servizio_id):
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    eventi_collection = db['Evento']

    # Verifica se il servizio è presente in almeno un evento associato a un determinato fornitore
    evento_associato = eventi_collection.find_one({
        "servizi_associati": servizio_id,
        "isPagato": True
    })

    if evento_associato:
        # Gestisci la logica se il servizio è presente in un evento
        print("Il servizio è associato a un evento. Esegue la procedura di copia.")

        # Procedi con la procedura di copia del servizio
        servizio_corrente = servizi_collection.find_one({"_id": ObjectId(servizio_id)})

        if servizio_corrente:
            # Crea una copia del servizio corrente con le modifiche
            servizio_modificato = servizio_corrente.copy()
            campi_da_modificare = {k: v for k, v in nuovi_dati.items() if v is not None}
            servizio_modificato.update(campi_da_modificare)

            # Rimuovi temporaneamente il campo _id prima dell'inserimento
            servizio_modificato.pop('_id', None)

            # Inserisci il servizio modificato come nuovo documento
            result = servizi_collection.insert_one(servizio_modificato)

            # Ottieni l'ID del nuovo servizio appena inserito
            nuovo_servizio_id = result.inserted_id

            # Aggiorna il servizio corrente con l'ID del nuovo servizio
            servizi_collection.update_one(
                {"_id": ObjectId(servizio_id)},
                {"$set": {"isCurrentVersion": nuovo_servizio_id}}
            )

            # Restituisci l'ID del servizio appena inserito
            return nuovo_servizio_id

    else:
        # Il servizio non è associato a nessun evento, quindi modificalo direttamente
        servizio_corrente = servizi_collection.find_one({"_id": ObjectId(servizio_id)})

        if servizio_corrente:
            # Modifica direttamente il servizio
            campi_da_modificare = {k: v for k, v in nuovi_dati.items() if v is not None}
            servizi_collection.update_one(
                {"_id": ObjectId(servizio_id)},
                {"$set": campi_da_modificare}
            )

            # Restituisci l'ID del servizio modificato
            return servizio_id

    return None  # Ritorna None se il servizio corrente non esiste


def aggiungi_servizio(nuovi_dati):
    db = get_db()
    db['Servizio Offerto'].insert_one(nuovi_dati)


def Get_eventi_ByFornitorePrivato(id):
    from ..InterfacciaPersistenza import EventoPrivato
    print(id)
    db = get_db()
    eventi = db['Evento']
    eventi_fornitore_Privati = eventi.find({"fornitori_associati": id, "Ruolo": "2"})

    lista_eventi_fornitore = []
    for evento_fornitore in eventi_fornitore_Privati:
        eventoPrivato = EventoPrivato.Evento_Privato(evento_fornitore, evento_fornitore)
        lista_eventi_fornitore.append(eventoPrivato)

    return lista_eventi_fornitore


def GetEventi_FornitorePubblico(id):
    from ..InterfacciaPersistenza import EventoPubblico
    print(id)
    db = get_db()
    eventi = db['Evento']
    eventi_fornitore_Pubblico = eventi.find({"fornitori_associati": id, "Ruolo": "1"})

    lista_eventi_fornitore = []
    for evento_fornitore in eventi_fornitore_Pubblico:
        eventoPubblico = EventoPubblico.Evento_Pubblico(evento_fornitore, evento_fornitore)
        lista_eventi_fornitore.append(eventoPubblico)

    return lista_eventi_fornitore


def Cancella_evento(id):
    db = get_db()
    eventi = db['Evento']
    eventi.delete_one({"_id": ObjectId(id)})


def Get_dettagli_evento(id):
    from ..InterfacciaPersistenza import EventoPrivato
    db = get_db()
    eventi = db['Evento']
    evento_data = eventi.find_one({"_id": ObjectId(id)})
    evento = EventoPrivato.Evento_Privato(evento_data, evento_data)
    return evento


def Get_dati_organizzatore(id):
    from ..InterfacciaPersistenza import EventoPrivato
    db = get_db()
    eventi = db['Evento']
    evento_data = eventi.find_one({"_id": ObjectId(id)})
    evento = EventoPrivato.Evento_Privato(evento_data, evento_data)
    utenti = db['Utente']
    utenti_data = utenti.find_one({"_id": ObjectId(evento.organizzatore)})
    organizzatore = Organizzatore.Organizzatore(utenti_data, utenti_data)
    return organizzatore


def get_dati_servizi(id, id_fornitore):
    from ..InterfacciaPersistenza import EventoPrivato
    db = get_db()
    eventi = db['Evento']
    fornitori_db = db['Servizio Offerto']
    evento_data = eventi.find_one({"_id": ObjectId(id)})
    evento = EventoPrivato.Evento_Privato(evento_data, evento_data)
    servizi_lista = []
    for servizi in evento.servizi_associati:
        servizio_data = db['Servizio Offerto'].find_one({"_id": ObjectId(servizi)})
        print(servizio_data["Descrizione"])

        if servizio_data and ObjectId(servizio_data["fornitore_associato"]) == ObjectId(id_fornitore):
            print("rapa")
        else:
            servizi_lista.append(servizio_data)

    return servizi_lista


def invio_feedBack(id_valutato, id_valutante, valutazione):
    db = get_db()
    dati = {
        "id_valutato": id_valutato,
        "id_valutante": id_valutante,
        "valutazione": valutazione
    }
    db['FeedBack'].insert_one(dati)


def get_fornitori(id_fornitori):
    from ..InterfacciaPersistenza.Fornitore import Fornitore
    db = get_db()
    lista_id = [ObjectId(id_str) for id_str in id_fornitori]
    risultati = db['Utente'].find({'_id': {'$in': lista_id}})

    lista_fornitori = []
    # Iterazione sui risultati per aggiungere i fornitori alla lista
    for user_data in risultati:
        lista_fornitori.append(Fornitore(user_data, user_data))

    return lista_fornitori
