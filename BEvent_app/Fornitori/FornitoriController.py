from flask import Flask, render_template, Blueprint, request, session
from .FornitoriService import get_tutti_servizi, elimina, modifica, aggiungi
from BEvent_app import Routes
from flask import redirect, url_for
from ..Utils import Image
from ..Routes import home, fornitore_page

Fornitori = Blueprint('Fornitori', __name__)


@Fornitori.route('/fornitori')
def visualizza():  # put application's code here
    id_fornitore = session["id"]
    servizi = get_tutti_servizi(id_fornitore)

    return fornitore_page(servizi=servizi)


@Fornitori.route('/elimina_servizio/<servizio_id>')
def elimina_servizio(servizio_id):
    print(servizio_id)
    elimina(servizio_id)
    return redirect(url_for('Fornitori.visualizza'))


@Fornitori.route('/modifica/<servizio_id>', methods=['POST'])
def modifica_servizio(servizio_id):
    nuovi_dati = {
        "Descrizione": request.form.get("descrizione"),
        "Tipo": request.form.get("tipo"),
        "Prezzo": request.form.get("prezzo"),
        "DisponibilitàDataInizio": request.form.get("data_inizio"),
        "DisponibilitàDataFine": request.form.get("data_fine"),
        "Quantità": request.form.get("quantità"),
        "FotoServizo": request.form.get("foto_servizio"),
        "fornitore_associato": request.form.get("fornitore_associato")

    }

    modifica(nuovi_dati, servizio_id)
    return fornitore_page()


@Fornitori.route('/aggiungi_servizio', methods=['POST'])
def aggiungi_servizio():
    files = request.files.getlist('photos')

    byte_arrays = []

    for file in files:
        filename = file.filename
        content_type = file.content_type
        content = file.read()
        print(filename)

        byte_array = Image.convert_image_to_byte_array(content)
        byte_arrays.append(byte_array)

    byte_arrays_bytes = [bytes(byte_array) for byte_array in byte_arrays]

    nuovi_dati = {
        "Descrizione": request.form.get("descrizione"),
        "Tipo": request.form.get("tipo"),
        "Prezzo": request.form.get("prezzo"),
        "Quantità": request.form.get("quantità"),
        "FotoServizo": byte_arrays_bytes,
        "fornitore_associato": request.form.get("fornitore_associato")
    }

    aggiungi(nuovi_dati)
    return home()
