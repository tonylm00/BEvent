from datetime import datetime

from flask import request, Blueprint, session, flash, jsonify
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
        fornitori = GestioneEventoService.get_fornitori()
        servizi_offerti = GestioneEventoService.get_servizi()

        return sceltafornitori_page(fornitori=fornitori, servizi=servizi_offerti)
    else:
        flash("Errore nella data inserita")
        return scelta_evento_da_creare_page()


@ge.route('/filtro_categoria', methods=['POST'])
def filtro_categoria():
    try:
        data = request.get_json()

        if 'categoria' in data:
            categoria = data['categoria']
            servizi_filtrati, fornitori_filtrati = GestioneEventoService.filtro_categoria_liste(categoria)

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


@ge.route('/filtro_barra_ricerca', methods=['POST'])
def filtro_barra_ricerca():
    try:
        data = request.get_json()

        if 'ricerca' in data:
            ricerca = data['ricerca']
            servizi_filtrati, fornitori_filtrati = GestioneEventoService.filtro_ricerca(ricerca)

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

