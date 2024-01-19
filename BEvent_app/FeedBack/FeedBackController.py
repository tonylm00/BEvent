from flask import request, Blueprint, session, redirect, url_for
from .FeedBackService import  inserisci_recensione
fb = Blueprint('fb', __name__)


@fb.route('/invio_recensione', methods=['POST'])
def invio_recensione():

 id_valutato = request.form.get('id')
 id_valutante = session['id']
 voto = request.form.get('voto')
 titolo = request.form.get('titolo')
 descrizione = request.form.get('descrizione')
 inserisci_recensione(id_valutato,id_valutante,voto,titolo,descrizione)
 return redirect(url_for('aut.area_organizzatore'))
