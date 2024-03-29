from flask import render_template, Blueprint

# from flask_login import login_required, current_user
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/fornitore_page')
@login_required
def fornitore_page(servizi=None, dati=None, eventi_pubblici=None, eventi_privati=None):
    return render_template('AreaFornitore.html', servizi=servizi, dati=dati, eventiPrivati=eventi_privati,
                           eventiPubblici=eventi_pubblici)


@views.route('/organizzatore_page')
@login_required
def organizzatore_page(evento_privato=None, eventi_pubblici=None):
    return render_template('HomeOrganizzatore.html', evento_privato=evento_privato, eventi_pubblici=eventi_pubblici)


@views.route('/area_organizzatore_page')
@login_required
def area_organizzatore_page(organizzatore=None, eventi_privati=None, biglietti_comprati=None):
    return render_template('AreaOrganizzatore.html', organizzatore=organizzatore, eventi_privati=eventi_privati,
                           biglietti_comprati=biglietti_comprati)


@views.route('/home')
def home():
    return render_template('Home.html')


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
@login_required
def scelta_evento_da_creare_page():
    return render_template('SceltaEventoDaCreare.html')


@views.route('/SceltaFornitori_page')
@login_required
def sceltafornitori_page(fornitori=None, servizi=None, recensioni=None):
    return render_template('SceltaFornitori.html', fornitori=fornitori, servizi=servizi, recensioni=recensioni)


@views.route('/RicercaEventi_page')
def ricerca_eventi_page(eventi=None, eventi_sponsorizzati=None):
    return render_template('RicercaEventi.html', eventi=eventi, eventi_sponsorizzati=eventi_sponsorizzati)


@views.route('/RiepilogoScelte_page')
@login_required
def riepilogo_scelte_page(fornitori=None, servizi=None):
    return render_template('RiepilogoScelte.html', fornitori=fornitori, servizi=servizi)


@views.route('/EventoPublico_page')
@login_required
def crea_evento_pubblico_page(servizi=None, eventi_pubblici=None):
    return render_template('EventoPubblico.html', servizi=servizi, eventi_pubblici=eventi_pubblici)


@views.route('/Visualizza_evento_dettagli_page')
@login_required
def visualizza_evento_dettagli_page(evento=None, organizzatore=None, servizi=None):
    return render_template('EventoDettagli.html', evento=evento, organizzatore=organizzatore, servizi=servizi)


@views.route('/Visualizza_evento_dettagli_page_organizzatore')
@login_required
def visualizza_evento_dettagli_organizzatore_page(evento=None, organizzatore=None, servizi=None):
    return render_template('DettegliEventoPrivato.html', evento=evento, organizzatore=organizzatore, servizi=servizi)
