

from flask import Blueprint, flash

from BEvent_app.RicercaEvento.RicercaEventoService import get_eventi
from BEvent_app.Routes import ricerca_eventi_page, organizzatore_page

re = Blueprint('re', __name__)



@re.route('/visualizza_eventi', methods=['POST'])
def visualizza_eventi():

    eventi = get_eventi()
    if eventi:
        return ricerca_eventi_page(eventi=eventi)
    else:
        flash("Errore di sissstema")
        return organizzatore_page()

