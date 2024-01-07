from flask import Flask, render_template, Blueprint, request, session
from flask_login import current_user

from .FornitoriService import get_tutti_servizi, elimina, modifica, aggiungi, aggiorna_foto_fornitore, get_tutti_dati
from BEvent_app import Routes
from flask import redirect, url_for
from ..Utils import Image
from ..Routes import home, fornitore_page

Fornitori = Blueprint('Fornitori', __name__)


@Fornitori.route('/fornitori', methods=['GET', 'POST'])
def visualizza():  # put application's code here
    id_fornitore = session['id']
    dati = get_tutti_dati(id_fornitore)
    servizi = get_tutti_servizi(id_fornitore)
    return fornitore_page(servizi=servizi,dati=dati)


@Fornitori.route('/dati_fornitori', methods=['GET', 'POST'])
def visualizza_dati_fornitore():  # put application's code here
    id_fornitore = session['id']
    dati = get_tutti_dati(id_fornitore)
    return fornitore_page(dati=dati)


@Fornitori.route('/aggiungi_foto_fornitore', methods=['POST'])
def aggiungi_foto_fornitore():
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


@Fornitori.route('/elimina_servizio/<servizio_id>')
def elimina_servizio(servizio_id):
    elimina(servizio_id)
    return redirect(url_for('Fornitori.visualizza'))


@Fornitori.route('/modifica_servizio/', methods=['POST'])
def modifica_servizio():
    nuovi_dati = {
        "Descrizione": request.form.get("descrizione"),
        "Tipo": request.form.get("tipo"),
        "Prezzo": request.form.get("prezzo"),
        "Quantità": request.form.get("quantità"),
        "FotoServizio": request.form.get("foto_servizio"),
        "fornitore_associato":  session["id"]

    }
    print(nuovi_dati)
    modifica(nuovi_dati, request.form.get("servizio_id"))
    return visualizza()


@Fornitori.route('/aggiungi_servizio', methods=['POST'])
def aggiungi_servizio():
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

    nuovi_dati = {
        "Descrizione": request.form.get("descrizione"),
        "Tipo": request.form.get("tipo"),
        "Prezzo": request.form.get("prezzo"),
        "Quantità": request.form.get("quantità"),
        "FotoServizio": byte_arrays_bytes,
        "FotoServizio": byte_arrays_bytes,
        "fornitore_associato": fornitore_associato
    }

    aggiungi(nuovi_dati)
    return visualizza()