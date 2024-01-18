from flask import request, Blueprint, session, redirect
from .FeedBackService import  inserisci_recensione
fb = Blueprint('fb', __name__)


@fb.route('/invio_recensione', methods=['POST'])
def invio_recensione():
 print("invio_recensione")
 id_valutato = request.form.get('id')
 id_valutante = session['id']
 voto = request.form.get('voto')
 titolo = request.form.get('titolo')
 descrizione = request.form.get('descrizione')
 inserisci_recensione(id_valutato,id_valutante,voto,titolo,descrizione)
 return "fatto"
