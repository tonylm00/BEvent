import json
from datetime import datetime

from flask import request, Blueprint, session, flash, jsonify, make_response
from BEvent_app.GestioneEvento import GestioneEventoService
from BEvent_app.Routes import scelta_evento_da_creare_page, sceltafornitori_page

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
        fornitori = GestioneEventoService.get_fornitori(data_formattata)
        servizi_non_filtrati = GestioneEventoService.get_servizi(fornitori)
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
