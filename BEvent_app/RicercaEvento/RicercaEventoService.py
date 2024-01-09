from datetime import datetime

from ..db import get_db
from ..InterfacciaPersistenza.EventoPubblico import Evento_Pubblico


def get_eventi():
    db = get_db()
    eventi_collection = db['Evento']
    data_odierna = datetime.now().strftime("%Y-%m-%d")
    eventi_data = list(eventi_collection.find({
        "data_evento": {"$gt": data_odierna},
        "ruolo": 1
    }))

    lista_eventi = []

    for data in eventi_data:
        evento = Evento_Pubblico(data, data)
        lista_eventi.append(evento)

    return lista_eventi
