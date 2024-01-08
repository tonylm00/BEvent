from flask import Flask, render_template, Blueprint, request, session
from flask_login import current_user

from .FornitoriService import get_dati_fornitore, get_tutti_servizi_byFornitore,aggiorna_foto_fornitore,aggiungi_servizio,modifica_servizio,elimina_servizio
from BEvent_app import Routes
from flask import redirect, url_for
from ..Utils import Image
from ..Routes import home, fornitore_page


Fornitori = Blueprint('Fornitori', __name__)
def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_servizio_data(descrizione, tipo, prezzo, quantita):
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
def visualizza_controller():  # put application's code here
    id_fornitore = "6585cb448e551a0d24352c30"
    dati = get_dati_fornitore(id_fornitore)
    servizi = get_tutti_servizi_byFornitore(id_fornitore)
    return fornitore_page(servizi=servizi,dati=dati)

@Fornitori.route('/aggiungi_foto_fornitore', methods=['POST'])
def aggiungi_foto_fornitore_controller():
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


@Fornitori.route('/elimina_servizio/', methods=['POST'])
def elimina_servizio_controller():
    servizio_id = request.form.get('servizio_id')
    elimina_servizio(servizio_id)
    return redirect(url_for('Fornitori.visualizza'))


@Fornitori.route('/modifica_servizio/', methods=['POST'])
def modifica_servizio_controller():
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
    nuovi_dati = Fornitori(nuovi_dati)
    print(nuovi_dati)
    modifica_servizio(nuovi_dati, request.form.get("servizio_id"))
    return visualizza_controller()


@Fornitori.route('/aggiungi_servizio', methods=['POST'])
def aggiungi_servizio_controller():
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
        "fornitore_associato": fornitore_associato
    }
    aggiungi_servizio(nuovi_dati)
    return visualizza_controller()