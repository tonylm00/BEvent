from flask import request, Flask, Blueprint, session, redirect, url_for
from BEvent_app.Autenticazione import AutenticazioneService
from BEvent_app.Routes import login_page, home, admin_page, error_page, fornitore_page
from BEvent_app.Routes import login_page, home, registrazione_page

aut = Blueprint('aut', __name__)


@aut.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = AutenticazioneService.verify_user(email, password)
        if user:
            ruolo = user.get('Ruolo', None)
            nome = user.get('nome', None)
            session['ruolo'] = ruolo
            session['logged'] = True
            session['nome'] = nome
            if ruolo == "1":
                return admin_page()
            elif ruolo == "2":
                print("PROCVAAAAAAAA")
                return home()
            elif ruolo == "3":
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
        citta = request.form.get('citta')
        if AutenticazioneService.registra_org(nome, cognome, nome_utente, email, password, cpassword, telefono, data_di_nascita, citta,
                           ruolo):
            session["nome"] = nome_utente
            session["ruolo"] = ruolo

            return home()
    return registrazione_page()
