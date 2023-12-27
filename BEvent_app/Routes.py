from flask import render_template, Blueprint, session
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

def user_page():
    return render_template('AreaFornitore.html')

@views.route('/')
def home():
    return render_template('Home.html')

@views.route('/ruolo')
def ruolo_utente(ruolo_utente):
    if ruolo_utente == '3':
        return render_template('AreaFornitore.html')
    elif ruolo_utente == '2':
        return render_template('AreaOrganizzatore.html')
    elif ruolo_utente == '1':
        return render_template('AreaAdmin.html')
    else:
        return "Ruolo non riconosciuto."

@views.route('/login_page')
def login_page():
    return render_template('Login.html')


@views.route('/registrazione_page')
def registrazione_page():
    if not current_user.is_authenticated:
        return render_template('Registrazione.html')
    return home()

