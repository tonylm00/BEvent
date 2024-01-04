from datetime import datetime

from flask import flash

from ..db import get_db
from ..InterfacciaPersistenza.Fornitore import Fornitore
from ..InterfacciaPersistenza.ServizioOfferto import Servizio_Offerto


def is_valid_data(data):
    try:
        datetime_data = datetime.strptime(data, '%Y-%m-%d')
        data_odierna = datetime.now()
        if datetime_data > data_odierna:
            return True
        else:
            return False

    except ValueError:
        return False


def get_fornitori():
    db = get_db()
    fornitori_collection = db['Utente']
    fornitori_data = list(fornitori_collection.find({'Ruolo': '3'}))

    lista_fornitori = []

    for data in fornitori_data:
        fornitore = Fornitore(data, data)
        lista_fornitori.append(fornitore)

    return lista_fornitori


'''
def get_fornitori_by_tipo(tipo_desiderato):
    fornitori = get_fornitori()
    fornitori_filtrati = [fornitore for fornitore in fornitori if
                          fornitore.get("Fornitore", {}).get("Tipo") == tipo_desiderato]
    return fornitori_filtrati
'''


def get_servizi():
    db = get_db()
    servizi_collection = db['ServizioOfferto']
    servizi_data = list(servizi_collection.find())

    lista_servizi = []

    for data in servizi_data:
        servizio = Servizio_Offerto(data)
        lista_servizi.append(servizio)

    return lista_servizi


def filtro_categoria_liste(categoria):
    servizi_non_filtrati = get_servizi()
    fornitori_non_filtrati = get_fornitori()

    servizi_filtrati = [servizio for servizio in servizi_non_filtrati if servizio.tipo == categoria]

    id_fornitori = set(servizio.fornitore_associato for servizio in servizi_filtrati)

    fornitori_filtrati = [fornitore for fornitore in fornitori_non_filtrati if fornitore.id in id_fornitori]

    return servizi_filtrati, fornitori_filtrati


def filtrare_servizi_per_fornitore(servizi_non_filtrati, fornitori_filtrati):
    id_fornitori = set(fornitore.id for fornitore in fornitori_filtrati)

    servizi_filtrati = [servizio for servizio in servizi_non_filtrati if
                        servizio.fornitore_associato in id_fornitori]
    return servizi_filtrati


def filtro_ricerca(ricerca):
    servizi_non_filtrati = get_servizi()
    fornitori_non_filtrati = get_fornitori()

    fornitori_filtrati = [fornitore for fornitore in fornitori_non_filtrati if ricerca.lower() in fornitore.nome.lower()
                          ]

    if not fornitori_filtrati:
        fornitori_filtrati = [fornitore for fornitore in fornitori_non_filtrati if ricerca.lower() in
                              fornitore.descrizione.lower()]
        if not fornitori_filtrati:
            flash('Parola non trovata', 'error')
            return None, None

    servizi_filtrati = filtrare_servizi_per_fornitore(servizi_non_filtrati, fornitori_filtrati)

    return servizi_filtrati, fornitori_filtrati
