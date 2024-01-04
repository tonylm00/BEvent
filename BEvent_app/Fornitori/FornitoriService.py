from bson import ObjectId
from pymongo import MongoClient
from ..db import get_db


class Servizio:
    def __init__(self, _id, descrizione, tipo, prezzo, disponibilita_data_inizio, disponibilita_data_fine, quantita,
                 foto_servizio, fornitore_associato):
        self._id = _id
        self.descrizione = descrizione
        self.tipo = tipo
        self.prezzo = prezzo
        self.disponibilita_data_inizio = disponibilita_data_inizio
        self.disponibilita_data_fine = disponibilita_data_fine
        self.quantita = quantita
        self.foto_servizio = foto_servizio
        self.fornitore_associato = fornitore_associato

    def __repr__(self):
        return f"Servizio(_id={self._id}, descrizione={self.descrizione}, tipo={self.tipo}, prezzo={self.prezzo}, disponibilita_data_inizio={self.disponibilita_data_inizio}, disponibilita_data_fine={self.disponibilita_data_fine}, quantita={self.quantita}, foto_servizio={self.foto_servizio}, fornitore_associato={self.fornitore_associato})"


def get_tutti_servizi():
    db = get_db()
    servizi = db.ServizioOfferto.find({})

    return [Servizio(
        _id=str(servizio["_id"]) if "_id" in servizio else None,
        descrizione=servizio["Descrizione"],
        tipo=servizio["Tipo"],
        prezzo=servizio["Prezzo"],
        disponibilita_data_inizio=servizio["DisponibilitàDataInizio"],
        disponibilita_data_fine=servizio["DisponibilitàDataFine"],
        quantita=servizio["Quantità"],
        foto_servizio=servizio["FotoServizo"],
        fornitore_associato=servizio["fornitore_associato"]
    ) for servizio in servizi]


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
    db.ServizioOfferto.insert_one(nuovi_dati)
