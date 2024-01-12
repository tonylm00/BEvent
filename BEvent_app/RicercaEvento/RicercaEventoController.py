from flask import Blueprint, flash, request, jsonify

from BEvent_app.RicercaEvento.RicercaEventoService import get_eventi, ricerca_eventi_per_parola, serializza_eventi, \
    ricerca_eventi_per_categoria, ricerca_eventi_per_regione, ricerca_eventi_per_prezzo, get_evento_by_id
from BEvent_app.Routes import ricerca_eventi_page, organizzatore_page

re = Blueprint('re', __name__)


@re.route('/visualizza_eventi', methods=['POST'])
def visualizza_eventi():
    eventi = get_eventi()
    if eventi:
        return ricerca_eventi_page(eventi=eventi)
    else:
        flash("Errore di sissstema")
        return organizzatore_page()


@re.route('/filtro_barra_ricerca_eventi', methods=['POST'])
def filtro_barra_ricerca():
    try:
        data = request.get_json()
        if 'ricerca' in data:
            ricerca = data['ricerca']

            eventi_filtrati = ricerca_eventi_per_parola(ricerca)

            if eventi_filtrati:
                eventi_serializzati = [serializza_eventi(evento) for evento in eventi_filtrati]

                return jsonify({
                    'eventi_filtrati': eventi_serializzati
                }), 200
            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200
        else:
            return jsonify({"errore": "Parametro 'categoria' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@re.route('/filtro_categorie_eventi', methods=['POST'])
def filtro_categorie_eventi():
    try:
        data = request.get_json()
        if 'categoria' in data:
            categoria = data['categoria']

            eventi_filtrati = ricerca_eventi_per_categoria(categoria)

            if eventi_filtrati:
                eventi_serializzati = [serializza_eventi(evento) for evento in eventi_filtrati]

                return jsonify({
                    'eventi_filtrati': eventi_serializzati
                }), 200

            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'categoria' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@re.route('/filtro_regione_eventi', methods=['POST'])
def filtro_regione_eventi():
    try:
        data = request.get_json()
        if 'regione' in data:
            regione = data['regione']

            eventi_filtrati = ricerca_eventi_per_regione(regione)

            if eventi_filtrati:
                eventi_serializzati = [serializza_eventi(evento) for evento in eventi_filtrati]

                return jsonify({
                    'eventi_filtrati': eventi_serializzati
                }), 200

            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'categoria' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@re.route('/filtro_prezzo_eventi', methods=['POST'])
def filtro_prezzo_eventi():
    try:
        data = request.get_json()
        if 'prezzo_min' in data and 'prezzo_max' in data:
            prezzo_max = data['prezzo_max']
            prezzo_min = data['prezzo_min']

            eventi_filtrati = ricerca_eventi_per_prezzo(prezzo_min, prezzo_max)

            if eventi_filtrati:
                eventi_serializzati = [serializza_eventi(evento) for evento in eventi_filtrati]

                return jsonify({
                    'eventi_filtrati': eventi_serializzati
                }), 200

            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'categoria' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@re.route('/aggiorna_right_column_eventi', methods=['POST'])
def aggiorna_right_column_eventi():
    data = request.get_json()
    print(data)
    try:
        print("prova 1")
        if 'id_evento' in data:
            id_evento = data['id_evento']
            print("prova 2")

            evento_scelto = get_evento_by_id(id_evento)
            print("prova 3")
            if evento_scelto:
                print("prova 4")
                evento_serializzato = serializza_eventi(evento_scelto)
                print("prova 5")
                return jsonify({
                    "evento_scelto": evento_serializzato
                }), 200
            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'id_evento' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500
