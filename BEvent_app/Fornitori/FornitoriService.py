from bson import ObjectId
from pymongo import MongoClient

from ..InterfacciaPersistenza.Fornitore import Fornitore
from ..db import get_db
from ..InterfacciaPersistenza import ServizioOfferto


def get_tutti_servizi_byFornitore(id_fornitore):
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    servizi_data = list(servizi_collection.find({'fornitore_associato': id_fornitore,'isCurrentVersion': { '$in': [None, ''] }, 'isDeleted': False}))

    lista_servizi = []

    for data in servizi_data:
        servizio = ServizioOfferto.Servizio_Offerto(data)
        lista_servizi.append(servizio)

    return lista_servizi

def get_dati_fornitore(id_fornitore):
    db = get_db()
    user_data = db['Utente'].find_one({"_id":ObjectId(id_fornitore)})
    fornitore = Fornitore(user_data,user_data)
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
        "isPagato" : True
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



