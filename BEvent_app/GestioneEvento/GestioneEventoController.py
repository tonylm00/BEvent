from flask import request, Blueprint, session, flash
from BEvent_app.GestioneEvento import GestioneEventoService
from BEvent_app.Routes import sceltaeventodacreare_page, sceltafornitori_page

ge = Blueprint('ge', __name__)


@ge.route('/visualizza_fornitori', methods=['POST'])
def visualizza_fornitori():
    tipo_evento = request.form.get('tipo_evento')
    data = request.form.get('data_evento')
    n_invitati = request.form.get('n_invitati')

    session['tipo_evento'] = tipo_evento
    session['data_evento'] = data
    session['n_invitati'] = n_invitati

    if GestioneEventoService.is_valid_data(data):

        fornitori = GestioneEventoService.get_fornitori()
        return sceltafornitori_page(fornitori=fornitori)

    else:
        flash("Errore nella data inserita")
        return sceltaeventodacreare_page()


