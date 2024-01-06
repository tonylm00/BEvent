from bson import ObjectId
from pymongo import MongoClient

from ..InterfacciaPersistenza.Fornitore import Fornitore
from ..db import get_db
from ..InterfacciaPersistenza import ServizioOfferto


def get_tutti_servizi(id_fornitore):
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    servizi_data = list(servizi_collection.find({'fornitore_associato': id_fornitore}))

    lista_servizi = []

    for data in servizi_data:
        servizio = ServizioOfferto.Servizio_Offerto(data)
        lista_servizi.append(servizio)

    return lista_servizi

def get_tutti_dati(id_fornitore):
    db=get_db()
    user_data= db['Utente'].find({"_id":id_fornitore})
    fornitore= Fornitore(user_data,user_data)
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


def elimina(servizio_id):
    db = get_db()
    try:
        result = db.ServizioOfferto.delete_one({"_id": ObjectId(servizio_id)})
        print("Risultato eliminazione:", result.raw_result)
        return result.deleted_count
    except Exception as e:
        print("Errore durante l'eliminazione:", e)
        return 0


def modifica(nuovi_dati, servizio_id):
    db = get_db()
    result = db.ServizioOfferto.update_one(
        {"_id": ObjectId(servizio_id)},
        {"$set": nuovi_dati}
    )
    return result.modified_count


def aggiungi(nuovi_dati):
    db = get_db()
    db['Servizio Offerto'].insert_one(nuovi_dati)
