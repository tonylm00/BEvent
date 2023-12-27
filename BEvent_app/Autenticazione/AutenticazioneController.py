from flask import request, Flask, Blueprint, session
from flask_login import login_user

from BEvent_app.Autenticazione import AutenticazioneService
from BEvent_app.Routes import login_page, home, registrazione_page

aut = Blueprint('aut', __name__)


@aut.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = AutenticazioneService.verify_user(email, password)

        if user:
            # Autenticazione riuscita
            return home()
        else:
            return login_page()
    else:
        return login_page()


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
