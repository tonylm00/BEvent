import json
import os
from datetime import datetime
from importlib.metadata import files

from flask import request, Blueprint, session, flash, jsonify, make_response, redirect, url_for

from BEvent_app.FeedBack import FeedBackService
from BEvent_app.Fornitori import FornitoriService
from BEvent_app import Utils
from BEvent_app.GestioneEvento import GestioneEventoService
from BEvent_app.Routes import scelta_evento_da_creare_page, sceltafornitori_page, riepilogo_scelte_page, \
    visualizza_evento_dettagli_organizzatore_page, \
    organizzatore_page, crea_evento_pubblico_page
from ..Utils import Image


from flask import current_app as app

ge = Blueprint('ge', __name__)


@ge.route('/visualizza_fornitori', methods=['POST'])
def visualizza_fornitori():
    """
    Serve ad accedere alla pagina sceltafornitori.html passando in risposta i fornitori disponibili, i servizi e le
    recensioni relative a quei fornitori


    :return: Pagina 'sceltafornitori.html con tre liste di oggetti: fornitori(di tipo Fornitore), servizi( di tipo
    Servizio Offerto) e recensioni (di tipo Recensione)
    """
    tipo_evento = request.form.get('tipo_evento')
    data = request.form.get('data_evento')
    data_formattata = datetime.strptime(data, "%Y-%m-%d").strftime("%d-%m-%Y")
    n_invitati = request.form.get('n_invitati')

    session['tipo_evento'] = tipo_evento
    session['data_evento'] = data_formattata
    session['n_invitati'] = n_invitati

    if GestioneEventoService.is_valid_data(data):
        fornitori = GestioneEventoService.get_fornitori_disponibli(data_formattata)
        servizi_non_filtrati = GestioneEventoService.get_servizi(data_formattata)
        servizi_offerti = GestioneEventoService.filtrare_servizi_per_fornitore(servizi_non_filtrati, fornitori)
        recensioni = FeedBackService.get_recensioni_associate_a_servizi(servizi_offerti)

        return sceltafornitori_page(fornitori=fornitori, servizi=servizi_offerti, recensioni=recensioni)
    else:
        flash("Errore nella data inserita")
        return scelta_evento_da_creare_page()


@ge.route('/filtro_categoria', methods=['POST'])
def filtro_categoria():
    """
    Serve  a elaborare una richiesta in Ajax e in base alla categoria passata come parametro restituisce la lista dei
    servizi che appartengono a quel tipo e dei relativi fornitori

    :return: Risposta in formato JSON che continene due liste di oggetti: fornitori_filtrati(di tipo Fornitore) e
    servizi_filtrati( di tipo Servizio Offerto)
    """
    try:
        data = request.get_json()
        data_evento = session['data_evento']

        if 'categoria' in data:
            categoria = data['categoria']
            servizi_filtrati, fornitori_filtrati = GestioneEventoService.filtro_categoria_liste(categoria, data_evento)

            if servizi_filtrati and fornitori_filtrati:
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


@ge.route('/filtro_regione', methods=['POST'])
def filtro_regione():
    """
    Serve  a elaborare una richiesta in Ajax e in base alla regione passata come parametro restituisce la lista dei
    fornitori locati in quella regione e dei relativi servizi

    :return: Risposta in formato JSON che continene due liste di oggetti: fornitori_filtrati (di tipo Fornitore) e
    servizi_filtrati ( di tipo Servizio Offerto)
    """
    try:
        data = request.get_json()
        data_evento = session['data_evento']

        if 'regione' in data:
            regione = data['regione']
            servizi_filtrati, fornitori_filtrati = GestioneEventoService.filtro_regione_liste(regione, data_evento)

            if servizi_filtrati and fornitori_filtrati:
                fornitori_serializzati = [GestioneEventoService.fornitore_serializer(f) for f in fornitori_filtrati]
                servizi_serializzati = [GestioneEventoService.servizio_serializer(s) for s in servizi_filtrati]

                return jsonify({
                    "servizi_filtrati": servizi_serializzati,
                    "fornitori_filtrati": fornitori_serializzati
                }), 200
            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'regione' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@ge.route('/filtro_barra_ricerca', methods=['GET', 'POST'])
def filtro_barra_ricerca():
    """
    Serve  a elaborare una richiesta in Ajax e in base ad una parola passata come parametro restituisce la lista dei
    fornitori e dei servizi che contengono tale parola

    :return: Risposta in formato JSON che continene due liste di oggetti: fornitori(di tipo Fornitore) e servizi( di
    tipo Servizio Offerto)
    """
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
                    "fornitori_filtrati": fornitori_serializzati,
                }), 200
            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'categoria' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@ge.route('/filtro_prezzo', methods=['POST'])
def filtro_prezzo():
    """
    Serve  a elaborare una richiesta in Ajax e in base a un prezzo minimo e un prezzo massimo passati come parametri
    restituisce la lista dei servizi che hanno un prezzo compreso nel range e la lista dei relativi fornitori

    :return: Risposta in formato JSON che continene due liste di oggetti: fornitori(di tipo Fornitore) e servizi( di
    tipo Servizio Offerto)
    """
    try:
        data = request.get_json()
        data_evento = session['data_evento']

        if 'prezzo_min' in data and 'prezzo_max' in data:
            prezzo_max = data['prezzo_max']
            prezzo_min = data['prezzo_min']

            servizi_filtrati, fornitori_filtrati = GestioneEventoService.filtro_prezzo_liste(prezzo_min, prezzo_max,
                                                                                             data_evento)
            if servizi_filtrati and fornitori_filtrati:
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
    """
    Serve a elaborare una richiesta Ajax e in base all'email passata come parametro restituisce il singolo fornitore che
    corrisponde all'email e una lista con i suoi relativi servizi e le relative recensioni

    :return: Risposta in formato JSON che continene un oggetto e due liste di oggetti: oggetto fornitore_scelto(di tipo
    Fornitore), lista_servizi( lista di oggetti di tipo Servizio Offerto) e recensioni (lista di oggetti di tipo Recensione)
    """
    data = request.get_json()
    try:

        if 'email' in data:
            email = data['email']
            data_evento = session['data_evento']
            fornitore_scelto = GestioneEventoService.get_fornitore_by_email(email)

            if fornitore_scelto:
                lista_servizi = GestioneEventoService.get_servizi_fornitore(fornitore_scelto, data_evento)
                recensioni = FeedBackService.get_recensioni_associate_a_servizi(lista_servizi)
                recensioni_serializzate = [FeedBackService.recensione_serializer(r) for r in recensioni]
                servizi_serializzati = [GestioneEventoService.servizio_serializer(s) for s in lista_servizi]
                fornitore_serializzato = GestioneEventoService.fornitore_serializer(fornitore_scelto)

                return jsonify({
                    "lista_servizi": servizi_serializzati,
                    "fornitore_scelto": fornitore_serializzato,
                    "recensioni": recensioni_serializzate
                }), 200
            else:
                return jsonify({"errore": "nessuna corrispondenza nel db"}), 200

        else:
            return jsonify({"errore": "Parametro 'categoria' non presente nei dati JSON"}), 400

    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@ge.route('/salva_nel_carrello', methods=['POST'])
def salva_nel_carrello():
    """
    Serve a rispondere ad una richiesta Ajax e aggiungere ai cookie del carrello l'id del servizio che l'organizzatore
    vuole aggiungere al suo evento in modo che possa poi essere visualizzato e pagato in seguito. Se i cookie del
    carrello non sono ancora stati creati, li crea e fa in modo che durino un mese.

    :return: ritorna l'esito dell'operazione in formato JSON
    """
    data = request.get_json()
    try:
        if 'id_servizio' in data:
            id_servizio = data['id_servizio']
            if id_servizio != '':
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
        else:
            return jsonify({"errore nel passaggio del parametro"}), 500
    except Exception as e:
        return jsonify({"errore": str(e)}), 500


@ge.route('/visualizza_riepilogo', methods=['GET', 'POST'])
def visualizza_riepilogo():
    """
    Serve a visualizzare la pagina di riepilogo delle scelte effettuate dall'organizzatore durante la creazione
    dell'evento. Prende dai cookie i servizi precedentemente selezionati dall'organizzatore per ottenere la lista di
    servizi e relativi fornitori scelti.

    :return: Pagina riepilogoscelte.html con due liste: fornitori (lista di oggetti di tipo Fornitore) e servizi(lista
    di oggetti di tipo Servizio Offferto)
    """
    cookie_carrello = request.cookies.get('carrello')
    if cookie_carrello:

        carrello = json.loads(cookie_carrello)
        lista_servizi, lista_fornitori = GestioneEventoService.ottieni_servizi_e_fornitori_cookie(carrello)
    else:
        lista_servizi = None
        lista_fornitori = None

    return riepilogo_scelte_page(fornitori=lista_fornitori, servizi=lista_servizi)


@ge.route('/elimina_servizio', methods=['POST'])
def elimina_servizio():
    """
    Serve ad eliminare un servizio selezionato dai cookie.

    :return: redirect alla servlet visualizza riepilogo
    """
    id_servizio = request.form.get('id_servizio')

    carrello_cookie = request.cookies.get('carrello')
    carrello = json.loads(carrello_cookie)

    if id_servizio in carrello:
        carrello.remove(id_servizio)
        messaggio = "Servizio rimosso dal carrello"
    else:
        messaggio = "Servizio non trovato nel carrello"

    carrello_serializzato = json.dumps(carrello)
    response = make_response(redirect('/visualizza_riepilogo'))
    response.set_cookie('carrello', carrello_serializzato, httponly=True, path='/', max_age=60 * 60 * 24 * 31)

    return response


@ge.route("/annulla_creazione_evento", methods=['POST'])
def annulla_creazione_evento():
    """
    Serve ad annullare la creazione di un evento, eliminando dalla sessione i dati inseriti durante la creazione ed
    eliminando i cookie del carrello.

    :return: redirect alla pagina organizzatore
    """
    session.pop('data_evento', None)
    session.pop('tipo_evento', None)
    session.pop('n_invitati', None)

    response = make_response(redirect(url_for('aut.home_organizzatore')))
    response.set_cookie('carrello', '', expires=0, httponly=True)
    return response


@ge.route('/salva_evento_come_bozza', methods=['POST'])
def salva_evento_come_bozza():
    """
    Serve a salvare un evento come bozza nel database nel caso l'utente voglia proseguire in un secondo momento alla
    creazione effettiva dell'evento e quindi pagarlo. Rimuove dalla sessione i dati inseriti durante la creazione ed
    elimina i cookie del carrello.

    :return: redirect all'home organizzatore nel caso il salvataggio nel db vada a buon fine, altrimenti ritorna il
    redirect a visualizza riepilogo
    """
    result = salva_evento(is_pagato=False)

    if result:
        session.pop('data_evento', None)
        session.pop('tipo_evento', None)
        session.pop('n_invitati', None)
        response = make_response(redirect(url_for('views.organizzatore_page')))
        response.set_cookie('carrello', '', expires=0, httponly=True)
        flash("Evento salvato con successo!", "success")
        return redirect(url_for('aut.home_organizzatore'))
    else:
        flash("Qualcosa è andato storto nella creazione dell'evento, riprova!", "error")
        return redirect('/visualizza_riepilogo')


@ge.route('/salva_evento_pagato', methods=['POST'])
def salva_evento_pagato():
    """
    Serve a salvare un evento nel database segnandolo come pagato, in modo che la prenotazione dei fornitori avvenga.
    Rimuove dalla sessione i dati inseriti durante la creazione ed elimina i cookie del carrello.

    :return: redirect all'home organizzatore nel caso il salvataggio nel db vada a buon fine, altrimenti ritorna il
    redirect a visualizza riepilogo
    """
    result = salva_evento(is_pagato=True)

    if result:
        session.pop('data_evento', None)
        session.pop('tipo_evento', None)
        session.pop('n_invitati', None)
        response = make_response(redirect(url_for('views.organizzatore_page')))
        response.set_cookie('carrello', '', expires=0, httponly=True)
        flash("Evento salvato con successo!", "success")
        return redirect(url_for('aut.home_organizzatore'))
    else:
        flash("Qualcosa è andato storto nella creazione dell'evento, riprova!", "error")
        return redirect('/visualizza_riepilogo')


def salva_evento(is_pagato):
    """
    Serve a salvare un evento nel database.

    :param is_pagato: (bool) indica se l'evento è stato pagato o meno
    :return: oggetto evento che rappresenta l'evento appena salvato nel database
    """
    cookie_carrello = request.cookies.get('carrello')
    data_evento = session['data_evento']
    tipo_evento = session['tipo_evento']
    n_invitati = session['n_invitati']
    descrizione = request.form.get('descrizione')
    nome_festeggiato = request.form.get('nome_festeggiato')
    prezzo = request.form.get('prezzo')
    ruolo = "2"
    id_organizzatore = session['id']

    file = request.files.get('photo')
    if file:
        foto_byte_array = Image.convert_image_to_byte_array(file.read())
    else:
        path_img = os.path.join(app.root_path, 'static', 'images', tipo_evento + '.jpg')
        with open(path_img, 'rb') as img_file:
            image_content = img_file.read()
        foto_byte_array = Image.convert_image_to_byte_array(image_content)

    carrello = json.loads(cookie_carrello)
    lista_servizi, lista_fornitori = GestioneEventoService.ottieni_servizi_e_fornitori_cookie(carrello)

    result = GestioneEventoService.save_evento(lista_servizi, lista_fornitori, tipo_evento, data_evento, n_invitati,
                                               nome_festeggiato, descrizione, is_pagato, ruolo, foto_byte_array, prezzo,
                                               id_organizzatore)

    return result


@ge.route('/elimina_evento_privato', methods=['POST'])
def elimina_evento_route():
    """
    Serve ad eliminare un evento privato.

    :return: redirect all'area organizzatore
    """
    id_evento = request.form.get('id_evento')
    successo, mail = GestioneEventoService.elimina_evento(id_evento)

    flash(mail, 'success' if successo else 'error')
    return redirect(url_for('aut.area_organizzatore'))


@ge.route('/Crea_evento_pubblico_page')
def creazione_evento_pubblico():
    """
    Serve a creare la pagina per creare un evento pubblico di un fornitore.

    :return: pagina creaeventopubblico.html
    """
    servizi = GestioneEventoService.get_tutti_servizi_byFornitoreLocation(session["id"])
    return crea_evento_pubblico_page(servizi=servizi)


@ge.route('/crea_evento_pubblico', methods=['POST'])
def crea_event_publico():
    """
    Serve a creare un evento pubblico.

    :return: messaggio di successo
    """
    file = request.files.get('fotinabella')
    content = file.read()
    print(file)
    foto_byte_array = Image.convert_image_to_byte_array(content)
    print(file)
    fornitore = FornitoriService.get_dati_fornitore(session["id"])
    Data = request.form.get('data')
    n_persone = request.form.get('n_persone')
    Descrizione = request.form.get('descrizione')
    Locandina = foto_byte_array
    Ruolo = '1'
    Tipo = request.form.get('tipo')
    isPagato = True
    fornitori_associati = [session['id']]
    servizi_associati = [request.form.get('servizi')]
    Prezzo = request.form.get('prezzo')
    Ora = request.form.get('ora')
    Nome = request.form.get('nome')
    via = fornitore.via
    Regione = fornitore.regione
    GestioneEventoService.crea_evento_pubblico(Data, n_persone, Descrizione, Locandina, Ruolo, Tipo, isPagato,
                                               fornitori_associati, servizi_associati, Prezzo, Ora, Nome, via, Regione,
                                               session["id"])
    return "fatto"


@ge.route('/acquista_biglietto', methods=['POST'])
def acquista_biglietto_controller():
    """
    Serve ad effettuare l'acquisto di un biglietto

    :return: redirect all'area organizzatore
    """
    id_evento = request.form.get('id')
    id_organizzatore = session["id"]
    GestioneEventoService.acquista_biglietto(id_evento, id_organizzatore)
    return redirect(url_for('aut.area_organizzatore'))


@ge.route('/Visuallizza_Dettagli_evento_Organizzatore', methods=['GET', 'POST'])
def visualizza_evento_dettagli_controller():
    """
    Serve a visualizzare i dettagli di un evento creato da un organizzatore

    :return: dettagliEventoPrivato.html con i parametri evento (oggetto di tipo evento priavto), organizzatore(oggetto
    di tipo Organizzatore) e servizi (lista di oggetti di tipo servizio offerto)
    """
    from ..Fornitori.FornitoriService import get_dettagli_evento, get_dati_organizzatore
    id = request.form.get("id")
    evento = get_dettagli_evento(id)
    organizzatore = get_dati_organizzatore(id)
    servizi = GestioneEventoService.get_dati_servizi_organizzatore(id)
    return visualizza_evento_dettagli_organizzatore_page(evento=evento, organizzatore=organizzatore, servizi=servizi)
