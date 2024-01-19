from flask import flash

from .. import get_db
from ..InterfacciaPersistenza.Recensione import Recensione
from bson import ObjectId
import re

db = get_db()


def get_recensioni_associate_a_servizi(servizi):
    """
    Ottiene le recensioni associate a una lista di servizi
    :param servizi: (list) lista di servizi di cui si vogliono ottenere le recensioni

    Returns: lista di recensioni associate ai servizi specificati
    """

    lista_id = [servizio._id for servizio in servizi]

    recensioni_data = list(db['Recensione'].find({'id_valutato': {'$in': lista_id}}))
    recensioni = []
    for data in recensioni_data:
        recensione = Recensione(data)
        recensioni.append(recensione)

    return recensioni


def recensione_serializer(recensione):
    """
    Serializza un ogetto Recensione di un dizionario
    :param recensione: (recensione) oggetto di recensio da serializzare

    Returns: dizinario contenete i dati serializzati della recensione

    """
    return {
        "id": recensione.id,
        "titolo": recensione.titolo,
        "nome_utente_valutante": recensione.nome_utente_valutante,
        "voto": recensione.voto,
        "descrizione": recensione.descrizione,
        "servizio": recensione.servizio
    }


def inserisci_recensione(id_valutato, id_valutante, voto, titolo, descrizione):
    if not isinstance(descrizione, str) or not len(descrizione) <= 100:
        flash("La descrizione della recensione è troppo lunga!", "error")
        return False
    elif not isinstance(voto, str) or not re.match(r'^[0-5]$', voto):
        flash("Il voto non è un numero che va da 0 a 5 ", "error")
        return False
    elif not isinstance(titolo, str) or not len(titolo) <= 30:
        flash("Il titolo della recensione è troppo lungo!", "error")
        return False
    else:
        recensioni = db["Recensione"]
        utenti = db["Utente"]
        servizi = db["Servizio Offerto"]
        utente_data = utenti.find_one({"_id": ObjectId(id_valutante)})
        servizio_data = servizi.find_one({"_id": ObjectId(id_valutato)})
        recensioni_data = {
            "id_valutato": str(id_valutato),
            "id_valutante": id_valutante,
            "Voto": voto,
            "Titolo": titolo,
            "Descrizione": descrizione,
            "Tipo_servizio_valutato": servizio_data["Tipo"],
            "Nome_utente_valutante": utente_data["nome"],
        }

        recensioni.insert_one(recensioni_data)

        flash("La recensione è stata scritta con successo!", "success")
        return True
