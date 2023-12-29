from flask import Flask, render_template, Blueprint
from .FornitoriService import get_tutti_servizi
from BEvent_app import Routes
from flask import redirect, url_for

Fornitori = Blueprint('Fornitori', __name__)


@Fornitori.route('/fornitori')
def visualizza():  # put application's code here

    servizi = get_tutti_servizi()
    for servizio in servizi:
        print("Documento Servizio:", servizio)
    return render_template('AreaFornitore.html', servizi=servizi)


@Fornitori.route('/elimina_servizio/<servizio_id>')
def elimina_servizio(servizio_id):
    elimina_servizio(servizio_id)
    return redirect(url_for('/fornitori'))
