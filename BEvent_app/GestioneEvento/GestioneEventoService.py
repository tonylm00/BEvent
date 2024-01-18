from datetime import datetime

import mail
from bson import ObjectId
from flask import flash

from ..InterfacciaPersistenza import ServizioOfferto
from ..InterfacciaPersistenza.EventoPrivato import Evento_Privato
from ..db import get_db
from ..InterfacciaPersistenza.Fornitore import Fornitore
from ..InterfacciaPersistenza.ServizioOfferto import Servizio_Offerto


def is_valid_data(data):
    """
    Funzione per verificare che la data inserita sia valida.

    :param data: (str) data inserita dall'utente nella pagina SceltaEventoDaCreare.html
    :return: True se la data è corretta, False altrimenti
    """
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
    """
    Funzione che ottiene tutti i fornitori che sono disponibili in una determinata data, prendendola dal database.
    Usa una pipeline per verificare quali sono disponibili.

    :param data_richiesta: (str) stringa che indica la data in cui si vuole creare un evento
    :return: lista di oggetti di tipo Fornitore, ovvero i fornitori disponibli
    """
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


def get_servizi(data_richiesta):
    """
    Funzione che ottiene dal database tutti i servizi che si possono prenotare in una determinata data, poichè alcuni
    potrebbero essere impegnati in un evento.

    :param data_richiesta: (str) stringa che indica la data in cui si vuole creare un evento
    :return: lista di oggetti di tipo Servizio Offerto, ovvero i servizi disponibli
    """

    db = get_db()
    servizi_collection = db['Servizio Offerto']
    eventi_collection = db['Eventi']

    servizi_data = list(servizi_collection.find({'$or': [{'isCurrentVersion': None}, {'isCurrentVersion': {'$exists': False}}]}))

    lista_servizi = []

    for data in servizi_data:
        servizio = Servizio_Offerto(data)
        evento_associato = eventi_collection.find_one({
            'servizi_associati': {'$in': [str(servizio._id)]},
            'Data': data_richiesta
        })

        if not evento_associato:
            lista_servizi.append(servizio)

    return lista_servizi


def filtro_categoria_liste(categoria, data):
    """
    Funzione per ottenere dal database la lista dei servizi che appartengono alla categiria specificata e la lista di
    fornitori che sono associati a quei servizi.

    :param categoria: (str) stringa che indica la categoria di servizio che si vuole filtrare
    :param data: (str) stringa che indica la data nel quale si vuole fare l'evento
    :return: due liste filtrate di oggetti: servizi filtrati (lista di oggetti di tipo Servizio Offerto) e fornitori
    filtrati (lista di oggetti di tipo Fornitore)
    """
    servizi = get_servizi(data)
    fornitori_non_filtrati = get_fornitori_disponibli(data)
    servizi_non_filtrati = filtrare_servizi_per_fornitore(servizi, fornitori_non_filtrati)

    servizi_filtrati = [servizio for servizio in servizi_non_filtrati if servizio.tipo == categoria]

    id_fornitori = set(servizio.fornitore_associato for servizio in servizi_filtrati)

    fornitori_filtrati = [fornitore for fornitore in fornitori_non_filtrati if fornitore.id in id_fornitori]

    return servizi_filtrati, fornitori_filtrati


def filtro_regione_liste(regione, data):
    servizi = get_servizi(data)
    fornitori_non_filtrati = get_fornitori_disponibli(data)

    fornitori_filtrati = [fornitore for fornitore in fornitori_non_filtrati if fornitore.regione == regione]

    servizi_filtrati = filtrare_servizi_per_fornitore(servizi, fornitori_filtrati)

    return servizi_filtrati, fornitori_filtrati


def filtro_prezzo_liste(prezzo_min, prezzo_max, data):
    servizi = get_servizi(data)
    fornitori_non_filtrati = get_fornitori_disponibli(data)
    servizi_non_filtrati = filtrare_servizi_per_fornitore(servizi, fornitori_non_filtrati)

    servizi_filtrati = [servizio for servizio in servizi_non_filtrati if prezzo_min <= servizio.prezzo <= prezzo_max]
    id_fornitori = set(servizio.fornitore_associato for servizio in servizi_filtrati)
    fornitori_filtrati = [fornitore for fornitore in fornitori_non_filtrati if fornitore.id in id_fornitori]

    return servizi_filtrati, fornitori_filtrati


def filtrare_servizi_per_fornitore(servizi_non_filtrati, fornitori_filtrati):
    id_fornitori = set(fornitore.id for fornitore in fornitori_filtrati)

    servizi_filtrati = [servizio for servizio in servizi_non_filtrati if
                        servizio.fornitore_associato in id_fornitori]
    return servizi_filtrati


def filtro_ricerca(ricerca, data):
    servizi = get_servizi(data)
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


def get_servizi_fornitore(fornitore, datarichiesta):

    servizi_non_filtrati = get_servizi(datarichiesta)

    lista_servizi = [servizio for servizio in servizi_non_filtrati if servizio.fornitore_associato == fornitore.id]

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
        if id_servizio != '' and id_servizio is not None:
            servizio = get_servizio_by_id(id_servizio)
            lista_servizi.append(servizio)

    lista_fornitori = []
    if lista_servizi:
        for servizio in lista_servizi:
            fornitore = get_fornitore_by_id(servizio.fornitore_associato)
            if fornitore not in lista_fornitori:
                lista_fornitori.append(fornitore)

    return lista_servizi, lista_fornitori


def crea_documento_evento_generico(data_evento, descrizione, tipo_evento, n_invitati, foto_byte_array, ruolo,
                                   id_fornitori, id_servizi, is_pagato):
    documento = {
        '_id': ObjectId(),
        'Data': data_evento,
        'Descrizione': descrizione,
        'Tipo': tipo_evento,
        'Invitati/Posti': n_invitati,
        'Locandina': foto_byte_array,
        'Ruolo': ruolo,
        'fornitori_associati': id_fornitori,
        'servizi_associati': id_servizi,
        'isPagato': is_pagato
    }

    return documento


def save_evento(lista_servizi, lista_fornitori, tipo_evento, data_evento, n_invitati, nome_festeggiato, descrizione,
                is_pagato, ruolo, foto_byte_array, prezzo, id_organizzatore):
    db = get_db()
    id_fornitori = [fornitore.id for fornitore in lista_fornitori]
    id_servizi = [servizio._id for servizio in lista_servizi]
    documento_evento_generico = crea_documento_evento_generico(data_evento, descrizione, tipo_evento, n_invitati,
                                                               foto_byte_array, ruolo, id_fornitori, id_servizi,
                                                               is_pagato)

    documento_evento_privato = {
        'EventoPrivato': {
            'Prezzo': prezzo,
            'Festeggiato/i': nome_festeggiato,
            'Organizzatore': id_organizzatore
        }
    }

    documento_evento = {**documento_evento_generico, **documento_evento_privato}
    db.Evento.insert_one(documento_evento)
    evento_privato = Evento_Privato(documento_evento_generico, documento_evento_privato)

    return evento_privato


def elimina_evento(id_evento):
    db = get_db()
    evento = db.Evento.find_one({"_id": ObjectId(id_evento)})

    evento_privato = Evento_Privato(evento, evento)
    if evento_privato is None:
        return False, "Evento non trovato"

    if evento_privato:
        evento_privato.notify_observers()

        # Eliminazione dell'evento
    db.Evento.delete_one({"_id": ObjectId(id_evento)})

    return True, "Evento eliminato e fornitori notificati"


def invia_email_fornitore(destinatario, oggetto, corpo):
    msg = mail(oggetto, sender="tuo@email.com", recipients=["Fornitore"])
    msg.body = corpo
    mail.send(msg)


def crea_evento_pubblico(Data, n_persone, Descrizione, locandina, Ruolo, Tipo, isPagato, fornitori_associati,
                         servizi_associati, prezzo, Ora, Nome, Via, Regione, id_fornitore):
    db = get_db()

    documento_evento_generico = crea_documento_evento_generico(Data, Descrizione, Tipo, n_persone,
                                                               locandina, Ruolo, fornitori_associati, servizi_associati,
                                                               isPagato)
    location = db.Utente.find_one({"_id": ObjectId(id_fornitore)})
    documento_evento_Pubblico = {
        'EventoPubblico': {
            'Prezzo': prezzo,
            'Nome': Nome,
            'Luogo': Via,
            'Regione': Regione,
            'Ora': Ora
        }
    }
    documento_evento = {**documento_evento_generico, **documento_evento_Pubblico}
    db.Evento.insert_one(documento_evento)


def get_tutti_servizi_byFornitoreLocation(id_fornitore):
    db = get_db()
    servizi_collection = db['Servizio Offerto']
    servizi_data = list(servizi_collection.find({
        'fornitore_associato': id_fornitore,
        'isCurrentVersion': {'$in': [None, '']},
        'isDeleted': False,
        'Tipo': 'Location'
    }))

    lista_servizi = []

    for data in servizi_data:
        servizio = ServizioOfferto.Servizio_Offerto(data)
        lista_servizi.append(servizio)

    return lista_servizi
