from flask import render_template, Blueprint
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/fornitore_page')
@login_required
def fornitore_page():
    return render_template('AreaFornitore.html')


@views.route('/organizzatore_page')
@login_required
def organizzatore_page():
    return render_template('HomeOrganizzatore.html')


@views.route('/admin_page')
@login_required
def admin_page():
    return render_template('AreaAdmin.html')

@views.route('/error_page')
def error_page():
    return render_template('ErrorPage.html')


@views.route('/home')
def home():
    return render_template('Home.html')


@views.route('/login_page')
def login_page():
    if not current_user.is_authenticated:
        return render_template('Login.html')
    return home()


@views.route('/registrazione_page')
def registrazione_page():
    if not current_user.is_authenticated:
        return render_template('Registrazione.html')
    return home()


@views.route('/creaEventoInizio_page')
@login_required
def creaeventoinizio_page():
    return render_template('CreazioneEventoIntro.html')


@views.route('/creaEventoMain_page')
@login_required
def creaeventomain_page(fornitori=None):
    return render_template('CreazioneEventoMain.html', fornitori=fornitori)
