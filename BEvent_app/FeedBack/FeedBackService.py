from .. import get_db
from ..InterfacciaPersistenza.Recensione import Recensione

from bson import ObjectId

def get_recensioni_associate_a_servizi(servizi):
    """
    Ottiene le recensioni associate a una lista di servizi
    :param servizi: (list) lista di servizi di cui si vogliono ottenere le recensioni

    Returns: lista di recensioni associate ai servizi specificati
    """
    db = get_db()

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
        "nome_utente_valutante": recensione.nome_utente_valutante,
        "voto": recensione.voto,
        "descrizione": recensione.descrizione,
        "servizio": recensione.servizio
    }

def inserisci_recensione(id_valutato,id_valutante,voto,titolo,descrizione):

    db =get_db()
    recensioni = db["Recensione"]
    utenti  =db["Utente"]
    servizi = db["Servizio Offerto"]
    print(id_valutato,id_valutante,voto,titolo,descrizione)
    utente_data = utenti.find_one({"_id": ObjectId(id_valutante)})
    servizio_data = servizi.find_one({"_id": ObjectId(id_valutato)})
    recensioni_data ={
        "id_valutato": id_valutato,
        "id_valutante": id_valutante,
        "Voto" : voto,
        "Titolo" : titolo,
        "Descrizione" : descrizione,
        "Tipo_servizio_valutato" : servizio_data["Tipo"],
        "Nome_utente_valutante" : utente_data["nome"],
    }

    recensioni.insert_one(recensioni_data)
