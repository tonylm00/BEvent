from datetime import datetime

from ..db import get_db
from ..InterfacciaPersistenza.EventoPubblico import Evento_Pubblico


def get_eventi():
    db = get_db()
    eventi_collection = db['Evento']
    data_odierna = datetime.now().strftime("%d-%m-%Y")
    eventi_data = list(eventi_collection.find({
        "Data": {"$gt": data_odierna},
        "Ruolo": "1"
    }))

    lista_eventi = []

    print(eventi_data)
    for data in eventi_data:
        evento = Evento_Pubblico(data, data)
        lista_eventi.append(evento)

    return lista_eventi
