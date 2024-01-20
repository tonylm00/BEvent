from flask import Blueprint, flash, request, jsonify, session
from flask_login import current_user

from BEvent_app.RicercaEvento.RicercaEventoService import get_eventi, ricerca_eventi_per_parola, serializza_eventi, \
    ricerca_eventi_per_categoria, ricerca_eventi_per_regione, ricerca_eventi_per_prezzo, get_evento_by_id, \
    serializza_eventi_column
from BEvent_app.Routes import ricerca_eventi_page, organizzatore_page

re = Blueprint('re', __name__)


@re.route('/visualizza_eventi', methods=['GET', 'POST'])
def visualizza_eventi():
    """
    Serve a visualizzare la pagina di ricerca degli eventi pubblici. Prende gli eventi pubblici e li restituisce come
    risposa nella pagina

    :return: ricercaeventi.html, con la lista di oggetti di tipo evento pubblico passata come parametro
    """
    eventi = get_eventi()
    if eventi:
        return ricerca_eventi_page(eventi=eventi)
    else:
        flash("Errore di sissstema")
        return organizzatore_page()


@re.route('/filtro_barra_ricerca_eventi', methods=['POST'])
def filtro_barra_ricerca():
    """
    Serve  a elaborare una richiesta in Ajax e in base ad una parola passata come parametro restituisce la lista degli
    eventi che contengono tale parola.

    :return:  Risposta in formato JSON che contiene una lista di oggetti: eventi_filtrati(di tipo Evento Pubblico)
    """
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
    """
    Serve  a elaborare una richiesta in Ajax e in base alla categoria passata come parametro restituisce la lista degli
    eventi che appartengono a quel tipo

    :return: risposta in formato JSON che continene una lista di eventi filtrati: eventi_filtrati(lista di oggetti di
    tipo evento Pubblico)
    """
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
    """
    Serve  a elaborare una richiesta in Ajax e in base alla regione passata come parametro restituisce la lista degli
    eventi che si trovano in quella regione

    :return: Risposta in formato JSON che continene una lista di oggetti: eventi_filtrati (di tipo Evento Pubblico)
    """
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
    """
    Serve  a elaborare una richiesta in Ajax e in base a un prezzo minimo e un prezzo massimo passati come parametri
    restituisce la lista dei eventi che hanno un prezzo compreso nel range

    :return: Risposta in formato JSON che continene una lista di oggetti: eventi_filtrati(di tipo Evento Pubblico)
    """
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
    """
    Serve a elaborare una richiesta Ajax e in base all'id dell'evento passato come parametro restituisce il singolo
    evento che corrisponde all'id

    :return: Risposta in formato JSON che continene un oggetto: evento (oggetto di tipo Evento Pubblico)
    """
    if current_user.is_authenticated:
        nome_utente = session['nome_utente']
    else:
        nome_utente = None

    data = request.get_json()
    try:

        if 'id_evento' in data:
            id_evento = data['id_evento']

            evento_scelto = get_evento_by_id(id_evento)

            if evento_scelto:

                evento_serializzato = serializza_eventi_column(evento_scelto, nome_utente)

                return jsonify({
                    "evento_scelto": evento_serializzato
                }), 200
            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'id_evento' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500
