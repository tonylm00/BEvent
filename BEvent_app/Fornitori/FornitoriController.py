from flask import Flask, render_template, Blueprint, request, session
from flask_login import current_user
from ..InterfacciaPersistenza.ServizioOfferto import Servizio_Offerto
from .FornitoriService import get_dati_fornitore, get_tutti_servizi_byFornitore,aggiorna_foto_fornitore,aggiungi_servizio,modifica_servizio,elimina_servizio,get_eventi_ByFornitorePrivato,getEventi_FornitorePubblico,cancella_evento,get_dettagli_evento,get_dati_organizzatore,get_dati_servizi,invio_feedBack
from BEvent_app import Routes
from flask import redirect, url_for
from ..Utils import Image
from ..Routes import home, fornitore_page,visualizza_evento_dettagli_page


Fornitori = Blueprint('Fornitori', __name__)
def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_servizio_data(descrizione, tipo, prezzo, quantita):
    '''
    serve un validare i dati di servizio

    :param descrizione: str
    :param tipo: str
    :param prezzo: float
    :param quantita: int

    :return: messaggi di errore nel caso in cui uno dei campi non è valido ( con annessa descrizione del problema ),
    True se invece i campi sono validi

    '''
    # Verifica se la descrizione supera i 500 caratteri
    if len(descrizione) > 500:
        return False, "La descrizione non deve superare i 500 caratteri."

    # Verifica se il tipo supera i 25 caratteri
    if len(tipo) > 25:
        return False, "Il tipo non deve superare i 25 caratteri."

    # Verifica se il prezzo è un numero positivo
    if not is_valid_number(prezzo) or float(prezzo) < 0:
        return False, "Il prezzo deve essere un numero non negativo."

    # Verifica se la quantità è un numero intero positivo
    if not quantita.isdigit() or int(quantita) < 0:
        return False, "La quantità deve essere un numero intero non negativo."

    return True, None


@Fornitori.route('/fornitori', methods=['GET', 'POST'])
def visualizza_controller():
    '''
    serve a visualizzare tutti i dati relativi agli eventi( sia pubblici che privati ),servizi offerti, generalità  del fornitore

    :return: Pagina del fornitore AreaFornitore.Html
    '''
    id_fornitore = session["id"]
    dati = get_dati_fornitore(id_fornitore)
    servizi = get_tutti_servizi_byFornitore(id_fornitore)
    eventiPrivati = get_eventi_ByFornitorePrivato(id_fornitore)
    eventiPubblici = getEventi_FornitorePubblico(id_fornitore)

    return fornitore_page(servizi=servizi, dati=dati, eventiPrivati=eventiPrivati,eventiPubblici=eventiPubblici)

@Fornitori.route('/aggiungi_foto_fornitore', methods=['POST'])

def aggiungi_foto_fornitore_controller():
    '''

    :return:
    '''
    files = request.files.getlist('foto')
    id_fornitore = session['id']

    byte_arrays = []

    for file in files:
        filename = file.filename
        content_type = file.content_type
        content = file.read()

        byte_array = Image.convert_image_to_byte_array(content)
        byte_arrays.append(byte_array)

    byte_arrays_bytes = [bytes(byte_array) for byte_array in byte_arrays]

    aggiorna_foto_fornitore(id_fornitore, byte_arrays_bytes)

    return redirect('/fornitori')


@Fornitori.route('/elimina_servizio_areaFornitore/', methods=['POST'])
def elimina_servizio_controller():
    '''

    :return:
    '''
    servizio_id = request.form.get('servizio_id')
    elimina_servizio(servizio_id)
    return redirect('/fornitori')


@Fornitori.route('/modifica_servizio/', methods=['POST'])
def modifica_servizio_controller():
    '''

    :return:
    '''
    descrizione = request.form.get("descrizione")
    tipo = request.form.get("tipo")
    prezzo = request.form.get("prezzo")
    quantita = request.form.get("quantità")
    is_valid, error_message = validate_servizio_data(descrizione, tipo, prezzo, quantita)
    if not is_valid: return error_message
    nuovi_dati = {
        "Descrizione": descrizione,
        "Tipo": tipo,
        "Prezzo": prezzo,
        "Quantità": quantita,
        "FotoServizio": request.form.get("foto_servizio"),
        "fornitore_associato": session["id"]
    }
    print(request.form.get("servizio_id"))
    modifica_servizio(nuovi_dati, request.form.get("servizio_id"))
    return redirect('/fornitori')


@Fornitori.route('/aggiungi_servizio', methods=['POST'])
def aggiungi_servizio_controller():
    '''

    :return:
    '''
    files = request.files.getlist('photos')
    fornitore_associato = session['id']
    byte_arrays = []

    for file in files:
        filename = file.filename
        content_type = file.content_type
        content = file.read()

        byte_array = Image.convert_image_to_byte_array(content)
        byte_arrays.append(byte_array)

    byte_arrays_bytes = [bytes(byte_array) for byte_array in byte_arrays]
    descrizione = request.form.get("descrizione")
    tipo = request.form.get("tipo")
    prezzo = request.form.get("prezzo")
    quantita = request.form.get("quantità")
    is_valid, error_message = validate_servizio_data(descrizione, tipo, prezzo, quantita)
    if not is_valid: return error_message
    nuovi_dati = {
        "Descrizione": descrizione,
        "Tipo":  tipo,
        "Prezzo": prezzo,
        "Quantità": quantita,
        "FotoServizio": byte_arrays_bytes,
        "fornitore_associato": fornitore_associato,
        "isDeleted": False,
        "isCurrentVersion" : None
    }
    aggiungi_servizio(nuovi_dati)
    return redirect('/fornitori')

@Fornitori.route('/elimina_evento_pubblico', methods=['POST'])
def elimina_evento_controller():
    '''

    :return:
    '''
    id = request.form.get("id")
    cancella_evento(id)
    return redirect('/fornitori')


@Fornitori.route('/Visuallizza_Dettagli_evento_Fornitore',  methods=['GET', 'POST'])
def visualizza_evento_dettagli_controller():
    id = request.form.get("id")
    evento = get_dettagli_evento(id)
    organizzatore = get_dati_organizzatore(id)
    servizi = get_dati_servizi(id,session["id"])
    return visualizza_evento_dettagli_page(evento = evento, organizzatore =organizzatore, servizi=servizi)
@Fornitori.route('/invio_Feedback', methods=['POST'])
def invio_FeedBack_controller():
    id = request.form.get("valutato")
    valutazione = request.form.get("valutazione")
    invio_feedBack(id, session["id"], valutazione)
    return redirect("/fornitori")
