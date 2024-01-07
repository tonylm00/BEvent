from datetime import datetime

from bson import ObjectId
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


def get_fornitori_disponibli(data_richiesta):
    db = get_db()

    pipeline = [
        {"$match": {"Ruolo": "3"}},
        {
            "$lookup": {
                "from": "Evento",
                "let": {"fornitore_id_str": {"$toString": "$_id"}},
                "pipeline": [
                    {
                        "$unwind": "$Evento.fornitori_associati"
                    },
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$$fornitore_id_str", "$Evento.fornitori_associati"]},
                                    {"$eq": ["$Evento.Data", data_richiesta]},
                                    {"$eq": ["$Evento.isPagato", True]}
                                ]
                            }
                        }
                    }
                ],
                "as": "eventi_associati"
            }
        },
        {
            "$addFields": {
                "eventiPrenotati": {"$size": "$eventi_associati"},
                "EventiMassimiGiornaliero": "$Fornitore.EventiMassimiGiornaliero"
            }
        },
        {
            "$match": {
                "$expr": {"$lt": ["$eventiPrenotati", "$EventiMassimiGiornaliero"]}
            }
        }
    ]

    fornitori_disponibili = list(db.Utente.aggregate(pipeline))
    lista_fornitori = []

    for data in fornitori_disponibili:
        fornitore = Fornitore(data, data)
        lista_fornitori.append(fornitore)

    return lista_fornitori


def get_servizi():
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    servizi_data = list(servizi_collection.find({}))

    lista_servizi = []

    for data in servizi_data:
        servizio = Servizio_Offerto(data)
        lista_servizi.append(servizio)

    return lista_servizi


def filtro_categoria_liste(categoria, data):
    servizi = get_servizi()
    fornitori_non_filtrati = get_fornitori_disponibli(data)
    servizi_non_filtrati = filtrare_servizi_per_fornitore(servizi, fornitori_non_filtrati)

    servizi_filtrati = [servizio for servizio in servizi_non_filtrati if servizio.tipo == categoria]

    id_fornitori = set(servizio.fornitore_associato for servizio in servizi_filtrati)

    fornitori_filtrati = [fornitore for fornitore in fornitori_non_filtrati if fornitore.id in id_fornitori]

    return servizi_filtrati, fornitori_filtrati


def filtrare_servizi_per_fornitore(servizi_non_filtrati, fornitori_filtrati):
    id_fornitori = set(fornitore.id for fornitore in fornitori_filtrati)

    servizi_filtrati = [servizio for servizio in servizi_non_filtrati if
                        servizio.fornitore_associato in id_fornitori]
    return servizi_filtrati


def filtro_ricerca(ricerca, data):
    servizi = get_servizi()
    fornitori_non_filtrati = get_fornitori_disponibli(data)
    servizi_non_filtrati = filtrare_servizi_per_fornitore(servizi, fornitori_non_filtrati)

    fornitori_filtrati_nome = [fornitore for fornitore in fornitori_non_filtrati if
                               ricerca.lower() in fornitore.nome_utente.lower()
                               ]

    fornitori_filtrati_desctizione = [fornitore for fornitore in fornitori_non_filtrati if ricerca.lower() in
                                      fornitore.descrizione.lower()]

    fornitori_filtrati = None
    if fornitori_filtrati_desctizione and fornitori_filtrati_nome:
        fornitori_unici = {}

        for fornitore in fornitori_filtrati_nome + fornitori_filtrati_desctizione:
            fornitori_unici[fornitore.id] = fornitore

        fornitori_filtrati = list(fornitori_unici.values())
    elif fornitori_filtrati_desctizione:
        fornitori_filtrati = fornitori_filtrati_desctizione
    elif fornitori_filtrati_nome:
        fornitori_filtrati = fornitori_filtrati_nome

    if fornitori_filtrati:
        servizi_filtrati = filtrare_servizi_per_fornitore(servizi_non_filtrati, fornitori_filtrati)
    else:
        servizi_filtrati = None

    return servizi_filtrati, fornitori_filtrati


def get_fornitore_by_email(email):
    db = get_db()
    fornitore_data = db['Utente'].find_one({"email": email})
    fornitore = Fornitore(fornitore_data, fornitore_data)
    return fornitore


def get_servizi_fornitore(fornitore):
    db = get_db()
    servizi_data = list(db['Servizio Offerto'].find({"fornitore_associato": fornitore.id}))

    lista_servizi = []

    for data in servizi_data:
        servizio = Servizio_Offerto(data)
        lista_servizi.append(servizio)

    return lista_servizi


def fornitore_serializer(fornitore):
    return {
        "id": fornitore.id,
        "nome": fornitore.nome,
        "foto": fornitore.foto,
        "citta": fornitore.citta,
        "regione": fornitore.regione,
        "OrarioDiLavoro": fornitore.orario_lavoro,
        "email": fornitore.email,
        "nome_utente": fornitore.nome_utente,
        "descrizione": fornitore.descrizione
    }


def servizio_serializer(servizio):
    return {
        "id": servizio._id,
        "tipo": servizio.tipo,
        "fornitore_associato": servizio.fornitore_associato,
        "descrizione": servizio.descrizione,
        "prezzo": servizio.prezzo,
        "foto_servizio": servizio.foto_servizio
    }


def get_servizio_by_id(id_servizio):
    db = get_db()
    id_servizio_obj = ObjectId(id_servizio)
    servizio_data = db["Servizio Offerto"].find_one({"_id": id_servizio_obj})
    servizio = Servizio_Offerto(servizio_data)
    return servizio


def get_fornitore_by_id(id_fornitore):
    db = get_db()
    id_fornitore_obj = ObjectId(id_fornitore)
    fornitore_data = db['Utente'].find_one({"_id": id_fornitore_obj})
    fornitore = Fornitore(fornitore_data, fornitore_data)
    return fornitore


def ottieni_servizi_e_fornitori_cookie(carrello):
    lista_servizi = []

    for id_servizio in carrello:
        servizio = get_servizio_by_id(id_servizio)
        lista_servizi.append(servizio)

    lista_fornitori = []
    if lista_servizi:
        for servizio in lista_servizi:
            fornitore = get_fornitore_by_id(servizio.fornitore_associato)
            lista_fornitori.append(fornitore)

    return lista_servizi, lista_fornitori

'''
def save_evento(lista_servizi, lista_fornitori, tipo_evento, data_evento, n_invitati, nome_festeggiato, descrizione,
                is_pagato, ruolo, foto_byte_array):

'''