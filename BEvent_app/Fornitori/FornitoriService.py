from bson import ObjectId
from pymongo import MongoClient

from ..InterfacciaPersistenza.Fornitore import Fornitore
from ..db import get_db
from ..InterfacciaPersistenza import ServizioOfferto


def get_tutti_servizi_byFornitore(id_fornitore):
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    servizi_data = list(servizi_collection.find({'fornitore_associato': id_fornitore, 'isCurrentVersion': True,'isDeleted': False}))

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
            {"$set": {"Fornitore.Foto": byte_arrays_bytes}}
        )
        if result.modified_count > 0:
            return "Foto aggiornata con successo"
        else:
            return "Nessun documento aggiornato"
    except Exception as e:
        return f"Si è verificato un errore: {e}"


def elimina_servizio(servizio_id):
    db = get_db()
    servizi = db['Servizio Offerto']
    result = servizi.update_one(
            {"_id": ObjectId(servizio_id)},
            {"$set": {"isDeleted": True}}
        )
    return result


def modifica_servizio(nuovi_dati, servizio_id):
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    servizio_corrente = servizi_collection.find_one({"_id": ObjectId(servizio_id)})
    if servizio_corrente:
        servizi_collection.update_one(
            {"_id": ObjectId(servizio_id)},
            {"$set": {"isCurrentVersion": False}}
        )
    servizio_modificato = servizio_corrente.copy()
    campi_da_modificare = {k: v for k, v in nuovi_dati.items() if v is not None}
    servizio_modificato.update(campi_da_modificare)

    servizio_modificato["isCurrentVersion"] = True;
    db['Servizio Offerto'].insert_one(servizio_modificato)



def aggiungi_servizio(nuovi_dati):
    db = get_db()
    db['Servizio Offerto'].insert_one(nuovi_dati)


