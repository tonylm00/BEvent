from flask import Blueprint, request, session
from flask_login import login_required
from .FornitoriService import get_dati_fornitore, get_tutti_servizi_byfornitore, aggiorna_foto_fornitore, \
    aggiungi_servizio, modifica_servizio, elimina_servizio, get_eventi_by_fornitore_privato, \
    get_eventi_fornitore_pubblico, \
    cancella_evento, get_dettagli_evento, get_dati_organizzatore, get_dati_servizi, invio_feed_back, sponsorizza
from flask import redirect
from ..Utils import Image
from ..Routes import fornitore_page, visualizza_evento_dettagli_page

Fornitori = Blueprint('Fornitori', __name__)


@Fornitori.route('/fornitori', methods=['GET', 'POST'])
@login_required
def visualizza_controller():
    """
    serve a visualizzare tutti i dati relativi agli eventi( sia pubblici che privati ),servizi offerti, generalità
    del fornitore :return: Pagina del fornitore AreaFornitore.Html
    """
    id_fornitore = session["id"]
    dati = get_dati_fornitore(id_fornitore)
    servizi = get_tutti_servizi_byfornitore(id_fornitore)
    eventi_privati = get_eventi_by_fornitore_privato(id_fornitore)
    eventi_pubblici = get_eventi_fornitore_pubblico(id_fornitore)

    return fornitore_page(servizi=servizi, dati=dati, eventi_privati=eventi_privati, eventi_pubblici=eventi_pubblici)


@Fornitori.route('/aggiungi_foto_fornitore', methods=['POST'])
@login_required
def aggiungi_foto_fornitore_controller():
    """
    Aggiunge una foto al fornitore
    :return: reindirizza alla a pagina del fornitore
    """
    files = request.files.getlist('foto')
    id_fornitore = session['id']

    byte_arrays = []

    for file in files:

        content = file.read()

        byte_array = Image.convert_image_to_byte_array(content)
        byte_arrays.append(byte_array)

    byte_arrays_bytes = [bytes(byte_array) for byte_array in byte_arrays]

    aggiorna_foto_fornitore(id_fornitore, byte_arrays_bytes)

    return redirect('/fornitori')


@Fornitori.route('/elimina_servizio_areaFornitore/', methods=['POST'])
@login_required
def elimina_servizio_controller():
    """
    Elimina servizio scelto dal fornitore
    :return: reindirizza alla a pagina del fornitore
    """
    servizio_id = request.form.get('servizio_id')
    elimina_servizio(servizio_id)
    return redirect('/fornitori')


@Fornitori.route('/modifica_servizio/', methods=['POST'])
@login_required
def modifica_servizio_controller():
    """
    Modifica servizio scelto dal fornitore
    :return: reindirizza alla a pagina del fornitore
    """
    descrizione = request.form.get("descrizione")
    tipo = request.form.get("tipo")
    prezzo = request.form.get("prezzo")
    quantita = request.form.get("quantità")
    nuovi_dati = {
        "Descrizione": descrizione,
        "Tipo": tipo,
        "Prezzo": prezzo,
        "Quantità": quantita,
        "FotoServizio": request.form.get("foto_servizio"),
        "fornitore_associato": session["id"]
    }
    modifica_servizio(nuovi_dati, request.form.get("servizio_id"))
    return redirect('/fornitori')


@Fornitori.route('/aggiungi_servizio', methods=['POST'])
@login_required
def aggiungi_servizio_controller():
    """
    Serve ad aggiungerere un servizio nell'aria del fornitore :return: reindirizza all'area fornitore nel caso in cui
    tutti i campi rispettino le condizioni altrimenti restituisce un errore
    """
    files = request.files.getlist('photos')
    fornitore_associato = session['id']
    byte_arrays = []

    for file in files:

        content = file.read()

        byte_array = Image.convert_image_to_byte_array(content)
        byte_arrays.append(byte_array)

    byte_arrays_bytes = [bytes(byte_array) for byte_array in byte_arrays]
    descrizione = request.form.get("descrizione")
    tipo = request.form.get("tipo")
    prezzo = request.form.get("prezzo")
    nuovi_dati = {
        "Descrizione": descrizione,
        "Tipo": tipo,
        "Prezzo": prezzo,
        "FotoServizio": byte_arrays_bytes,
        "fornitore_associato": fornitore_associato,
        "isDeleted": False,
        "isCurrentVersion": None
    }
    result = aggiungi_servizio(nuovi_dati)
    if result:
        return redirect('/fornitori')
    else:
        return "errore"


@Fornitori.route('/elimina_evento_pubblico', methods=['POST'])
@login_required
def elimina_evento_controller():
    """
    elimina un evento pubblico
    :return: reindirizza alla a pagina del fornitore
    """
    id = request.form.get("id")
    cancella_evento(id)
    return redirect('/fornitori')


@Fornitori.route('/Visuallizza_Dettagli_evento_Fornitore', methods=['GET', 'POST'])
@login_required
def visualizza_evento_dettagli_controller():
    """
    Visualizza i dettagli dell'evento in cui è stato prenotato il servizio del fornitore
    :return: reindirizza alla pagina dettagli dell'evento

    """
    id = request.form.get("id")
    evento = get_dettagli_evento(id)
    organizzatore = get_dati_organizzatore(id)
    servizi = get_dati_servizi(id, session["id"])
    return visualizza_evento_dettagli_page(evento=evento, organizzatore=organizzatore, servizi=servizi)


@Fornitori.route('/invio_Feedback', methods=['POST'])
@login_required
def invio_feedback_controller():
    """
    Permette l'inserimento di un feedback al servizio offerto di un altro fornitore
    :return: reindirizza alla a pagina del fornitore

    """
    id = request.form.get("valutato")
    valutazione = request.form.get("valutazione")
    invio_feed_back(id, session["id"], valutazione)
    return redirect("/fornitori")


@Fornitori.route('/sponsorizza_evento', methods=['POST'])
@login_required
def sponsorizza_evento():
    """
    permette di sponsorizzare un evento
    :return: reindirizza alla a pagina del fornitore

    """
    id_evento = request.form.get("id_evento")
    sponsorizza(id_evento)
    return redirect("/fornitori")
