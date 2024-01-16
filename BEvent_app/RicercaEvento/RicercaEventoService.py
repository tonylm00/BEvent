from datetime import datetime

from bson import ObjectId, Int64

from ..db import get_db
from ..InterfacciaPersistenza.EventoPubblico import Evento_Pubblico



def get_eventi():
    db = get_db()
    eventi_collection = db['Evento']
    data_odierna = datetime.now().strftime("%d-%m-%Y")
    eventi_data = list(eventi_collection.find({
        "Data": {"$gt": data_odierna},
        "Ruolo": "1",
        "EventoPubblico.BigliettiDisponibili": {"$ne": "0"}
    }))

    lista_eventi = []

    print(eventi_data)
    for data in eventi_data:
        evento = Evento_Pubblico(data, data)
        lista_eventi.append(evento)

    return lista_eventi


def serializza_eventi(evento):
    print(evento.biglietti_disponibili)
    evento = {
        'data': evento.data,
        'descrizione': evento.descrizione,
        'n_persone': evento.n_persone,
        'locandina': evento.locandina,
        'tipo': evento.tipo,
        'fornitori_associati': evento.fornitori_associati,
        'servizi_associati': evento.servizi_associati,
        'isPagato': evento.isPagato,
        'prezzo': evento.prezzo,
        'nome': evento.nome,
        'regione': evento.regione,
        'luogo': evento.luogo,
        'ora': evento.ora,
        'biglietti_disponibili': evento.biglietti_disponibili
    }
    return evento


def ricerca_eventi_per_parola(ricerca):
    eventi_non_filtrati = get_eventi()

    eventi_filtrati_nome = [evento for evento in eventi_non_filtrati if ricerca.lower() in evento.nome]

    eventi_filtrati_descrizione = [evento for evento in eventi_non_filtrati if ricerca.lower() in evento.descrizione]

    eventi_filtrati = None
    if eventi_filtrati_nome and eventi_filtrati_descrizione:
        eventi_unici = {}
        for evento in eventi_filtrati_nome + eventi_filtrati_descrizione:
            eventi_unici[evento.id] = evento

        eventi_filtrati = list(eventi_unici.values())

    elif eventi_filtrati_nome:
        eventi_filtrati = eventi_filtrati_nome

    elif eventi_filtrati_descrizione:
        eventi_filtrati = eventi_filtrati_descrizione

    return eventi_filtrati


def ricerca_eventi_per_categoria(categoria):
    eventi_non_filtrati = get_eventi()

    eventi_filtrati = [evento for evento in eventi_non_filtrati if categoria.lower() == evento.tipo]

    return eventi_filtrati


def ricerca_eventi_per_regione(regione):
    eventi_non_filtrati = get_eventi()

    eventi_filtrati = [evento for evento in eventi_non_filtrati if regione.lower() == evento.regione]

    return eventi_filtrati


def ricerca_eventi_per_prezzo(prezzo_min, prezzo_max):
    eventi_non_filtrati = get_eventi()

    eventi_filtrati = [evento for evento in eventi_non_filtrati if prezzo_min <= evento.prezzo <= prezzo_max]

    return eventi_filtrati


def get_evento_by_id(id_evento):
    db = get_db()
    evento_scelto_data = db['Evento'].find_one({'_id': ObjectId(id_evento)})
    evento = Evento_Pubblico(evento_scelto_data, evento_scelto_data)
    return evento
