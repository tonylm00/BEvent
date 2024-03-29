from datetime import datetime
from flask import flash
from bson import ObjectId
from ..db import get_db
from ..InterfacciaPersistenza.EventoPubblico import EventoPubblico


def get_eventi():
    """
    Funzione che recupera dal database i documenti della collezione evento. Una volta recuperati li filtra in modo che
    la loro data sia maggiore della data odierna, che il ruolo sia 1 così che siano eventi pubblici e controllando che
    il numero si biglietti disponibili non sia zero.

    :return: lista_eventi (lista di oggetti di tipo Evento Pubblico)
    """
    db = get_db()
    eventi_collection = db['Evento']
    data_odierna = datetime.now().strftime("%d-%m-%Y")
    eventi_data = list(eventi_collection.find({
        "$expr": {
            "$gt": [
                {
                    "$dateFromString": {
                        "dateString": "$Data",
                        "format": "%d-%m-%Y"
                    }
                },
                {
                    "$dateFromString": {
                        "dateString": data_odierna,
                        "format": "%d-%m-%Y"
                    }
                }
            ]
        },
        "Ruolo": "1",
        "EventoPubblico.BigliettiDisponibili": {"$ne": "0"}
    }))
    lista_eventi = []

    for data in eventi_data:
        evento = EventoPubblico(data, data)
        lista_eventi.append(evento)

    return lista_eventi


def get_eventi_sponsorizzati():
    """
       Ottiene una lista di eventi sponsorizzati che soddisfano determinati criteri.

       :return: List[EventoPubblico]
           Una lista di oggetti EventoPubblico rappresentanti gli eventi sponsorizzati.

       """
    db = get_db()
    eventi_collection = db['Evento']
    data_odierna = datetime.now().strftime("%d-%m-%Y")
    eventi_data = list(eventi_collection.find({
        "$expr": {
            "$gt": [
                {
                    "$dateFromString": {
                        "dateString": "$Data",
                        "format": "%d-%m-%Y"
                    }
                },
                {
                    "$dateFromString": {
                        "dateString": data_odierna,
                        "format": "%d-%m-%Y"
                    }
                }
            ]
        },
        "Ruolo": "1",
        "isPagato": True,
        "EventoPubblico.BigliettiDisponibili": {"$ne": "0"}
    }))
    lista_eventi_sponsorizzati = []

    for data in eventi_data:
        evento = EventoPubblico(data, data)
        lista_eventi_sponsorizzati.append(evento)

    return lista_eventi_sponsorizzati


def serializza_eventi(evento):
    """
     Funzione per serializzare un oggetto della classe fornitore in modo che sia passabile come risposta json.

    :param evento: (obj) oggetto della classe Evento Pubblico che contiene i dati dell'evento scelto

    :return: dizionario che rappresenta i dati dell'oggetto evento pubblico
    """
    evento = {
        'id': evento.id,
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


def serializza_eventi_column(evento, nome_utente):
    """
        Serializza un oggetto evento in un formato adatto per l'inserimento in una colonna.

        :param evento: Oggetto evento
            L'oggetto evento da serializzare.

        :param nome_utente: str
            Il nome utente associato all'evento.

        :return: dict
            Un dizionario contenente i dettagli serializzati dell'evento.

        """
    evento = {
        'id': evento.id,
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
        'biglietti_disponibili': evento.biglietti_disponibili,
        'nome_utente': nome_utente
    }
    return evento


def ricerca_eventi_per_parola(ricerca):
    """
    Funzione per ottenere dal database la lista eventi pubblici la cui descrizione o nome contiene la parola inserita
    dall'organizzatore.
    -Viene presa la lista di eventi successivi alla data odierna.
    -Vengono filtrati gli eventi cercando la parola sia nel nome che nella descrizione, creando la lista di eventi da
    restituire

    :param ricerca: (str) stringa che indica la parola da ricercare

    :return: una lista filtrata di oggetti: eventi_filtrati (lista di oggetti di tipo Evento Pubblico)
   """
    eventi_non_filtrati = get_eventi()

    eventi_filtrati_nome = [evento for evento in eventi_non_filtrati if ricerca.lower() in evento.nome.lower()]

    eventi_filtrati_descrizione = [evento for evento in eventi_non_filtrati if
                                   ricerca.lower() in evento.descrizione.lower()]

    eventi_filtrati = None
    if eventi_filtrati_nome and eventi_filtrati_descrizione:
        eventi_unici = {}
        for evento in eventi_filtrati_nome + eventi_filtrati_descrizione:
            eventi_unici[evento.id] = evento

        eventi_filtrati = list(eventi_unici.values())
        flash("evento trovato", category="success")

    elif eventi_filtrati_nome:
        eventi_filtrati = eventi_filtrati_nome
        flash("evento trovato", category="success")

    elif eventi_filtrati_descrizione:
        eventi_filtrati = eventi_filtrati_descrizione
        flash("evento trovato", category="success")
    else:
        flash("nessun evento trovato", category="warning")

    return eventi_filtrati


def ricerca_eventi_per_categoria(categoria):
    """
    Funzione per ottenere dal database la lista di eventi che appartengono alla categoria inserita dall'utente.
    -Viene presa la lista di tutti gli eventi successivi alla data odierna.
    -La lista degli eventi viene filtrata per prendere gli eventi che hanno il parametro "tipo" che corrisponde
    alla categoria indicata.

    :param categoria: (str) stringa che indica la categoria di eventi che si vuole filtrare

    :return: una lista filtrata di oggetti: eventi_filtrati (lista di oggetti di tipo Evento Pubblico)
   """
    if categoria not in ['Conferenze e Seminari', 'Concerti e Spettacoli', 'Mostre ed Esposizioni', 'Corsi e Workshop',
                         'Eventi Benefici', 'Eventi Sociali']:
        if categoria == "Annulla":
            return get_eventi()
        else:
            flash("La categoria non esiste", category="error")
            return []
    elif categoria in ['Conferenze e Seminari', 'Concerti e Spettacoli', 'Mostre ed Esposizioni', 'Corsi e Workshop',
                       'Eventi Benefici', 'Eventi Sociali']:
        flash("La categoria esiste", category="success")

        eventi_non_filtrati = get_eventi()

        eventi_filtrati = [evento for evento in eventi_non_filtrati if categoria.lower() == evento.tipo.lower()]
        return eventi_filtrati


def ricerca_eventi_per_regione(regione):
    """
    Funzione per ottenere dal database la lista di eventi che si trovano nella regione inserita dall' organizzatore.
    -Viene presa la lista di tutti gli eventi successivi alla data odierna.
    -La lista degli eventi viene filtrata per prendere gli eventi che hanno il parametro "regione" che corrisponde alla
    regione indicata.

    :param regione: (str) stringa che indica la regione a cui devono appartenere gli eventi

    :return: una lista filtrata di oggetti: eventi_filtrati (lista di oggetti di tipo Evento Pubblico)
    """
    if regione not in ['Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia Romagna', 'Friuli Venezia Giulia',
                       'Lazio', 'Liguria', 'Lombardia', 'Marche', 'Molise', 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia',
                       'Toscana', 'Trentino Alto Adige', 'Umbria', 'Valle d Aosta', 'Veneto']:
        if regione == 'Annulla':
            return get_eventi()
        else:
            flash("La regione non esiste", category="error")
            return []
    elif regione in ['Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia Romagna', 'Friuli Venezia Giulia',
                     'Lazio', 'Liguria', 'Lombardia', 'Marche', 'Molise', 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia',
                     'Toscana', 'Trentino Alto Adige', 'Umbria', 'Valle d Aosta', 'Veneto']:
        flash("La regione esiste", category="success")

    eventi_non_filtrati = get_eventi()

    eventi_filtrati = [evento for evento in eventi_non_filtrati if regione.lower() == evento.regione.lower()]

    return eventi_filtrati


def ricerca_eventi_per_prezzo(prezzo_min, prezzo_max):
    """
    Funzione per ottenere dal database la lista eventi il cui prezzo si trova nel range di prezzo
    inserito dall'organizzatore.
    -Viene presa la lista di tutti gli eventi successivi alla data odierna.
    -La lista degli eventi viene filtrata per prendere gli eventi che rientrano nel range di prezzi indicati dall'
    organizzatore.

    :param prezzo_min: (str) stringa che indica il prezzo minimo del range di prezzo scelto dall'organizzatore
    :param prezzo_max: (str) stringa che indica il prezzo massimo del range di prezzo scelto dall'organizzatore

    :return: una lista filtrata di oggetti: eventi_filtrati (lista di oggetti di tipo Evento Pubblico)
   """
    if prezzo_min == "" and prezzo_max == "":
        return get_eventi()
    elif prezzo_min == "" and int(prezzo_max) >= 0:
        prezzo_min = 0
        eventi_non_filtrati = get_eventi()
        eventi_filtrati = [evento for evento in eventi_non_filtrati if float(prezzo_min) <= float(evento.prezzo) <=
                           float(prezzo_max)]
        return eventi_filtrati
    elif int(prezzo_min) >= 0 and prezzo_max == "":

        eventi_non_filtrati = get_eventi()
        eventi_filtrati = [evento for evento in eventi_non_filtrati if float(prezzo_min) <= float(evento.prezzo)]
        return eventi_filtrati
    if int(prezzo_min) <= 0 or int(prezzo_max) <= 0:
        flash("il prezzo minore o massimo è negativo", category="error")
        return []
    elif int(prezzo_min) > 0 and int(prezzo_max) > 0:
        flash("il prezzo minore o massimo non è negativo", category="success")

        eventi_non_filtrati = get_eventi()
        eventi_filtrati = [evento for evento in eventi_non_filtrati if float(prezzo_min) <= float(evento.prezzo) <=
                           float(prezzo_max)]

        return eventi_filtrati


def get_evento_by_id(id_evento):
    """
    Funzione che ottiene dal database le informazioni dell'evento scelto, grazie all'id passato come parametro

    :param id_evento: (str) stringa che rappresenta l'id dell'evento che si vuole ottenere

    :return: oggetto evento di tipo EventoPubblico

    """
    db = get_db()
    evento_scelto_data = db['Evento'].find_one({'_id': ObjectId(id_evento)})
    evento = EventoPubblico(evento_scelto_data, evento_scelto_data)
    return evento
