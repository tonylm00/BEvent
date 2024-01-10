from flask import request, Blueprint, session, redirect, flash
from flask_login import login_user, logout_user, current_user
from BEvent_app.Autenticazione import AutenticazioneService
from BEvent_app.Autenticazione.AutenticazioneService import get_dati_area_organizzatore, get_dati_home_organizzatore
from BEvent_app.Routes import (home, registrazione_page, admin_page, error_page, organizzatore_page,
                               area_organizzatore_page)

aut = Blueprint('aut', __name__)


@aut.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = AutenticazioneService.verify_user(email, password)

        if user:

            login_user(user)

            session['id'] = current_user.get_id()
            session['ruolo'] = user.ruolo
            session['nome_utente'] = user.nome_utente
            session['regione'] = user.regione

            if user.ruolo == "1":
                return admin_page()
            elif user.ruolo == "2":
                return redirect('/home_organizzatore')
            elif user.ruolo == "3":
                session['is_location'] = user.isLocation
                return redirect('/fornitori')
            else:
                return error_page()
        else:
            return home()
    else:
        return home()


@aut.route('/logout')
def logout():
    session.pop('nome_utente', None)
    session.pop('ruolo', None)
    session.pop('regione', None)
    logout_user()
    return redirect('/')


@aut.route('/registrazione', methods=['POST'])
def registrazione_organizzatore():
    if request.method == 'POST':

        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        data_di_nascita = request.form.get('data_di_nascita')
        nome_utente = request.form.get('nome_utente')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        telefono = request.form.get('telefono')
        ruolo = request.form.get('ruolo')
        regione = request.form.get('regione')
        registrazione = 0

        if ruolo == "1":
            user = AutenticazioneService.registra_admin(nome, cognome, nome_utente, email, password, cpassword,
                                                        telefono, data_di_nascita, ruolo, regione)
            if user:
                login_user(user)
                registrazione = 1
                flash("Admin Registrato con successo", "success")
            else:
                flash("Admin non Registarto", "error")
        elif ruolo == "2":

            citta = request.form.get('citta')
            user = AutenticazioneService.registra_org(nome, cognome, nome_utente, email, password, cpassword, telefono,
                                                      data_di_nascita, citta, ruolo, regione)

            if user:
                login_user(user)
                registrazione = 1
                flash("Organizzatore Registrato con successo", "success")
            else:
                flash("Organizzatore non Registarto", "error")
        elif ruolo == "3":
            descrizione = request.form.get('descrizione')
            location = request.form.get('isLocation')
            eventi_max_giorn = request.form.get('eventi_max_giornaliero')
            citta = request.form.get('citta')
            via = request.form.get('via')
            piva = request.form.get('p_iva')
            islocation = False

            if location == "Si":
                islocation = True

            user = AutenticazioneService.registra_forn(nome, cognome, nome_utente, email, password, cpassword, telefono,
                                                       data_di_nascita, citta, ruolo, descrizione, islocation,
                                                       eventi_max_giorn, via, piva, regione)
            if user:
                login_user(user)
                session['is_location'] = user.isLocation
                registrazione = 1
                flash("Fornitore Registrato con Successo", "success")
            else:
                flash("Fornitore non registrato", "error")

        if registrazione == 1:
            session["nome_utente"] = nome_utente
            session["ruolo"] = ruolo
            session['regione'] = regione
            session['id'] = current_user.get_id()
            if ruolo == "1":
                return home()
            elif ruolo == "2":
                return redirect('/home_organizzatore')
            elif ruolo == "3":
                return redirect('/fornitori')

        else:
            return registrazione_page()


@aut.route('/area_organizzatore', methods=['POST'])
def area_organizzatore():
    id_organizzatore = session['id']

    organizzatore, eventi_privati, biglietti_comprati = get_dati_area_organizzatore(id_organizzatore)

    return area_organizzatore_page(organizzatore=organizzatore, eventi_privati=eventi_privati,
                                   biglietti_comprati=biglietti_comprati)


@aut.route('/home_organizzatore', methods=['GET', 'POST'])
def home_organizzatore():
    id_organizzatore = session['id']

    evento_privato, eventi_pubblici = get_dati_home_organizzatore(id_organizzatore)

    return organizzatore_page(evento_privato=evento_privato, eventi_pubblici=eventi_pubblici)
