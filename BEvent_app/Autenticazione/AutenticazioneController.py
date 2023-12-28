from flask import request, Flask, Blueprint, session, redirect, url_for, flash
from flask_login import login_user, logout_user
from BEvent_app.Autenticazione import AutenticazioneService
from BEvent_app.Routes import login_page, home, admin_page, error_page, fornitore_page
from BEvent_app.Routes import login_page, home, registrazione_page
from BEvent_app.InterfacciaPersistenza.Utente import Utente

aut = Blueprint('aut', __name__)



@aut.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = AutenticazioneService.verify_user(email, password)

        if user:

            login_user(user)

            session['ruolo'] = user.ruolo
            session['nomeutente'] = user.nome_utente

            if user.ruolo == "1":
                return admin_page()
            elif user.ruolo == "2":
                return home()
            elif user.ruolo == "3":
                return fornitore_page()
            else:
                return error_page()
        else:
            return login_page()
    else:
        return login_page()


@aut.route('/logout')
def logout():
    session.pop('logged', None)
    session.pop('nome', None)
    session.pop('ruolo', None)
    logout_user()
    return redirect('/')


@aut.route('/registrazione_organizzatore', methods=['GET', 'POST'])
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

        registrazione = 0

        if ruolo == "1":
            user = AutenticazioneService.registra_admin(nome, cognome, nome_utente, email, password, cpassword,
                                                        telefono, data_di_nascita, ruolo)
            if user:
                login_user(user)
                registrazione = 1
                flash("Admin Registrato con successo", "success")
            else:
                flash("Admin non Registarto", "error")
        elif ruolo == "2":
            citta = request.form.get('citta')
            user = AutenticazioneService.registra_org(nome, cognome, nome_utente, email, password, cpassword, telefono,
                                                      data_di_nascita, citta, ruolo)
            if user:
                login_user(user)
                registrazione = 1
                flash("Organizzatore Registrato con successo", "success")
            else:
                flash("Organizzatore non Registarto", "error")
        elif ruolo == "3":
            descrizione = request.form.get('descrizione')
            tipo = request.form.get('tipo')
            prezzo = request.form.get('prezzo')
            eventi_max_giorn = request.form.get('eventi_max_giornaliero')
            orario = request.form.get('orario_lavoro')
            quantita = request.form.get('quantita')
            citta = request.form.get('citta')
            via = request.form.get('via')
            piva = request.form.get('p_iva')

            user = AutenticazioneService.registra_forn(nome, cognome, nome_utente, email, password, cpassword, telefono,
                                                       data_di_nascita, citta, ruolo, descrizione, tipo, prezzo,
                                                       eventi_max_giorn, orario, quantita, via, piva)
            if user:
                login_user(user)
                registrazione = 1
                flash("Fornitore Registrato con Successo", "success")
            else:
                flash("Fornitore non registrato", "error")

        if registrazione == 1:
            session["nome"] = nome_utente
            session["ruolo"] = ruolo
            return home()
        else:
            return registrazione_page()
