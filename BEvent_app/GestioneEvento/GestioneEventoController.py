import json
from datetime import datetime

from flask import request, Blueprint, session, flash, jsonify, make_response, redirect
from BEvent_app.GestioneEvento import GestioneEventoService
from BEvent_app.Routes import scelta_evento_da_creare_page, sceltafornitori_page, riepilogo_scelte_page
from BEvent_app.Utils import Image

ge = Blueprint('ge', __name__)


@ge.route('/visualizza_fornitori', methods=['POST'])
def visualizza_fornitori():
    tipo_evento = request.form.get('tipo_evento')
    data = request.form.get('data_evento')
    data_formattata = datetime.strptime(data, "%Y-%m-%d").strftime("%d-%m-%Y")
    n_invitati = request.form.get('n_invitati')

    session['tipo_evento'] = tipo_evento
    session['data_evento'] = data_formattata
    session['n_invitati'] = n_invitati

    if GestioneEventoService.is_valid_data(data):
        fornitori = GestioneEventoService.get_fornitori_disponibli(data_formattata)
        servizi_non_filtrati = GestioneEventoService.get_servizi()
        servizi_offerti = GestioneEventoService.filtrare_servizi_per_fornitore(servizi_non_filtrati, fornitori)

        return sceltafornitori_page(fornitori=fornitori, servizi=servizi_offerti)
    else:
        flash("Errore nella data inserita")
        return scelta_evento_da_creare_page()


@ge.route('/filtro_categoria', methods=['POST'])
def filtro_categoria():
    try:
        data = request.get_json()
        data_evento = session['data_evento']

        if 'categoria' in data:
            categoria = data['categoria']
            servizi_filtrati, fornitori_filtrati = GestioneEventoService.filtro_categoria_liste(categoria, data_evento)

            if servizi_filtrati and fornitori_filtrati:
                return jsonify({
                    "servizi_filtrati": servizi_filtrati,
                    "fornitori_filtrati": fornitori_filtrati
                }), 200
            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'categoria' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500

@ge.route('/filtro_regione', methods=['POST'])
def filtro_regione():
    try:
        data = request.get_json()
        data_evento = session['data_evento']

        if 'regione' in data:
            regione = data['regione']
            servizi_filtrati, fornitori_filtrati = GestioneEventoService.filtro_regione_liste(regione, data_evento)

            if servizi_filtrati and fornitori_filtrati:
                return jsonify({
                    "servizi_filtrati": servizi_filtrati,
                    "fornitori_filtrati": fornitori_filtrati
                }), 200
            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'regione' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500

@ge.route('/filtro_barra_ricerca', methods=['GET', 'POST'])
def filtro_barra_ricerca():
    try:
        data = request.get_json()
        data_evento = session['data_evento']
        if 'ricerca' in data:
            ricerca = data['ricerca']

            servizi_filtrati, fornitori_filtrati = GestioneEventoService.filtro_ricerca(ricerca, data_evento)
            if servizi_filtrati or fornitori_filtrati:
                fornitori_serializzati = [GestioneEventoService.fornitore_serializer(f) for f in fornitori_filtrati]
                servizi_serializzati = [GestioneEventoService.servizio_serializer(s) for s in servizi_filtrati]

                return jsonify({
                    "servizi_filtrati": servizi_serializzati,
                    "fornitori_filtrati": fornitori_serializzati
                }), 200
            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'categoria' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500

@ge.route('CagatalogoEventi')
def CagatalogoEventi():

    return catalogo_eventi_page(eventi=eventi)

@ge.route('/aggiorna_right_column', methods=['POST'])
def aggiorna_right_column():
    data = request.get_json()
    try:

        if 'email' in data:
            email = data['email']

            fornitore_scelto = GestioneEventoService.get_fornitore_by_email(email)

            if fornitore_scelto:
                lista_servizi = GestioneEventoService.get_servizi_fornitore(fornitore_scelto)
                servizi_serializzati = [GestioneEventoService.servizio_serializer(s) for s in lista_servizi]
                fornitore_serializzato = GestioneEventoService.fornitore_serializer(fornitore_scelto)

                return jsonify({
                    "lista_servizi": servizi_serializzati,
                    "fornitore_scelto": fornitore_serializzato
                }), 200
            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'categoria' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@ge.route('/salva_nel_carrello', methods=['POST'])
def salva_nel_carrello():
    data = request.get_json()
    try:
        if 'id_servizio' in data:
            id_servizio = data['id_servizio']

            carrello_cookie = request.cookies.get('carrello')

            if carrello_cookie:
                carrello = json.loads(carrello_cookie)
            else:
                carrello = []

            if id_servizio not in carrello:
                carrello.append(id_servizio)
                messaggio = "Servizio aggiunto al carrello"
            else:
                messaggio = "Servizio già presente nel carrello"

            carrello_serializzato = json.dumps(carrello)

            response = make_response(jsonify(messaggio))
            response.set_cookie('carrello', carrello_serializzato, httponly=True, max_age=60 * 60 * 24 * 31)
            return response
        else:
            return jsonify({"errore nel passaggio del parametro"}), 500
    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@ge.route('/visualizza_riepilogo', methods=['POST'])
def visualizza_riepilogo():
    cookie_carrello = request.cookies.get('carrello')

    carrello = json.loads(cookie_carrello)
    print(carrello)

    lista_servizi, lista_fornitori = GestioneEventoService.ottieni_servizi_e_fornitori_cookie(carrello)

    return riepilogo_scelte_page(fornitori=lista_fornitori, servizi=lista_servizi)


@ge.route('/elimina_servizio', methods=['POST'])
def elimina_servizio():
    data = request.json.get('data')
    try:
        id_servizio = data['id_servizio']

        carrello_cookie = request.cookies.get('carrello')
        carrello = json.loads(carrello_cookie)

        if id_servizio in carrello:
            carrello.remove(id_servizio)
            messaggio = "Servizio rimosso dal carrello"
        else:
            messaggio = "Servizio non trovato nel carrello"

        carrello_serializzato = json.dumps(carrello)
        response = make_response(jsonify({"messaggio": messaggio}))
        response.set_cookie('carrello', carrello_serializzato, httponly=True, max_age=60 * 60 * 24 * 31)
        return redirect('/visualizza_riepilogo')
    except Exception as e:
        return jsonify({"errore": str(e)}), 500



'''
@ge.route('/aggiungi_foto_evento', methods=['POST'])
def aggiungi_foto_evento():
    file = request.files.get('photo')
    id_evento = request.form.get('id_evento')

    byte_arrays = []
    byte_array = Image.convert_image_to_byte_array(file.read())
    byte_arrays.append(byte_array)

    risultato = GestioneEventoService.aggiungi_foto(byte_arrays, id_evento)


@ge.route('/salva_evento_db', methods=['POST'])
def 
'''

'''
@ge.route('/salva_evento_come_bozza', methods=['POST'])
def salva_evento_come_bozza():
    cookie_carrello = request.cookies.get('carrello')
    data_evento = session['data_evento']
    tipo_evento = session['tipo_evento']
    n_invitati = session['n_invitati']
    descrizione = request.form.get('descrizione')
    nome_festeggiato = request.form.get('nome_festeggiato')

    is_pagato = False
    ruolo = "2"

    file = request.files.get('photo')
    if file:
        foto_byte_array = Image.convert_image_to_byte_array(file.read())
    else:
        path_img = "./static/images/" + tipo_evento + ".jpg"
        foto_byte_array = Image.convert_image_to_byte_array(path_img)

    carrello = json.loads(cookie_carrello)
    lista_servizi, lista_fornitori = GestioneEventoService.ottieni_servizi_e_fornitori_cookie(carrello)

    GestioneEventoService.save_evento(lista_servizi, lista_fornitori, tipo_evento, data_evento, n_invitati,
                                      nome_festeggiato, descrizione, is_pagato, ruolo, foto_byte_array)
'''