from datetime import datetime

from bson import ObjectId, Int64

from ..db import get_db
from ..InterfacciaPersistenza.EventoPubblico import Evento_Pubblico


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
    """
     Funzione per serializzare un oggetto della classe fornitore in modo che sia passabile come risposta json.

    :param evento: (obj) oggetto della classe Evento Pubblico che contiene i dati dell'evento scelto

    :return: dizionario che rappresenta i dati dell'oggetto evento pubblico
    """
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
    """
    Funzione per ottenere dal database la lista di eventi che appartengono alla categoria inserita dall'utente.
    -Viene presa la lista di tutti gli eventi successivi alla data odierna.
    -La lista degli eventi viene filtrata per prendere gli eventi che hanno il parametro "tipo" che corrisponde
    alla categoria indicata.

    :param categoria: (str) stringa che indica la categoria di eventi che si vuole filtrare

    :return: una lista filtrata di oggetti: eventi_filtrati (lista di oggetti di tipo Evento Pubblico)
   """
    eventi_non_filtrati = get_eventi()

    eventi_filtrati = [evento for evento in eventi_non_filtrati if categoria.lower() == evento.tipo]

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
    eventi_non_filtrati = get_eventi()

    eventi_filtrati = [evento for evento in eventi_non_filtrati if regione.lower() == evento.regione]

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
    eventi_non_filtrati = get_eventi()

    eventi_filtrati = [evento for evento in eventi_non_filtrati if prezzo_min <= evento.prezzo <= prezzo_max]

    return eventi_filtrati


def get_evento_by_id(id_evento):
    """
    Funzione che ottiene dal database le informazioni dell'evento scelto, grazie all'id passato come parametro

    :param id_evento: (str) stringa che rappresenta l'id dell'evento che si vuole ottenere

    :return: oggetto evento di tipo EventoPubblico

    """
    db = get_db()
    evento_scelto_data = db['Evento'].find_one({'_id': ObjectId(id_evento)})
    evento = Evento_Pubblico(evento_scelto_data, evento_scelto_data)
    return evento
