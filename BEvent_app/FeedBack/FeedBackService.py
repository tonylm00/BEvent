from .. import get_db
from ..InterfacciaPersistenza.Recensione import Recensione


def get_recensioni_associate_a_servizi(servizi):
    db = get_db()

    lista_id = [servizio._id for servizio in servizi]

    recensioni_data = list(db['Recensione'].find({'id_valutato': {'$in': lista_id}}))
    recensioni = []
    for data in recensioni_data:
        recensione = Recensione(data)
        recensioni.append(recensione)

    return recensioni


def recensione_serializer(recensione):
    return {
        "id": recensione.id,
        "nome_utente_valutante": recensione.nome_utente_valutante,
        "voto": recensione.voto,
        "descrizione": recensione.descrizione,
        "servizio": recensione.servizio
    }
