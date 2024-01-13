from flask import render_template, Blueprint, session
from flask_login import current_user

# from flask_login import login_required, current_user
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/fornitore_page')
# @login_required
def fornitore_page(servizi=None, dati=None, eventiPubblici=None,eventiPrivati=None):
    return render_template('AreaFornitore.html', servizi=servizi, dati=dati,eventiPrivati=eventiPrivati,eventiPubblici=eventiPubblici)


@views.route('/organizzatore_page')
# @login_required
def organizzatore_page(evento_privato=None, eventi_pubblici=None):
    return render_template('HomeOrganizzatore.html', evento_privato=evento_privato, eventi_pubblici=eventi_pubblici)


@views.route('/area_organizzatore_page')
# @login_required
def area_organizzatore_page(organizzatore=None, eventi_privati=None, biglietti_comprati=None):
    return render_template('AreaOrganizzatore.html', organizzatore=organizzatore, eventi_privati=eventi_privati,
                           biglietti_comprati=biglietti_comprati)


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


@views.route('/RicercaEventi_page')
# @login_required
def ricerca_eventi_page(eventi=None):
    return render_template('RicercaEventi.html', eventi=eventi)


@views.route('/RiepilogoScelte_page')
# @login_required
def riepilogo_scelte_page(fornitori=None, servizi=None):
    return render_template('RiepilogoScelte.html', fornitori=fornitori, servizi=servizi)
@views.route('/EventoPublico_page')
def crea_evento_pubblico_page(servizi=None):
    return render_template('EventoPubblico.html', servizi=servizi)

@views.route('/Visualizza_evento_dettagli_page')
def visualizza_evento_dettagli_page(evento=None,organizzatore=None,fornitori=None):
    return render_template('EventoDettagli.html', evento=evento, organizzatore=organizzatore,fornitori=fornitori)