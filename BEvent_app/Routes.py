from flask import render_template, Blueprint, session
from flask_login import current_user

# from flask_login import login_required, current_user
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/fornitore_page')
# @login_required
def fornitore_page(servizi=None):
    return render_template('AreaFornitore.html', servizi=servizi)


@views.route('/organizzatore_page')
# @login_required
def organizzatore_page():
    return render_template('HomeOrganizzatore.html')


@views.route('/area_organizzatore_page')
# @login_required
def area_organizzatore_page():
    return render_template('AreaOrganizzatore.html')


@views.route('/admin_page')
# @login_required
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


@views.route('/registrazione_organizzatore_page')
def registrazione_organizzatore_page():
    if not current_user.is_authenticated:
        return render_template('RegistrazioneOrganizzatore.html')
    return home()


@views.route('/scelta_evento_da_creare_page')
# @login_required
def scelta_evento_da_creare_page():
    return render_template('SceltaEventoDaCreare.html')


@views.route('/SceltaFornitori_page')
# @login_required
def sceltafornitori_page(fornitori=None, servizi=None):
    return render_template('SceltaFornitori.html', fornitori=fornitori, servizi=servizi)


@views.route('/TrovaEventi_page')
# @login_required
def trova_eventi_page():
    return render_template('TrovaEventi.html')


@views.route('/RiepilogoScelte_page')
# @login_required
def riepilogo_scelte_page(fornitori=None, servizi=None):
    return render_template('RiepilogoScelte.html', fornitori=fornitori, servizi=servizi)
