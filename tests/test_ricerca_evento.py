from flask import get_flashed_messages

from BEvent_app.RicercaEvento.RicercaEventoService import ricerca_eventi_per_parola, ricerca_eventi_per_categoria,ricerca_eventi_per_regione,ricerca_eventi_per_prezzo
from mock import mock_app
"""
test sulla lunghezza nella barra di ricerca
"""
def test_ricerca_evento_1_5_1(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')

        result=ricerca_eventi_per_parola("megaeventopubblicofantasticissimo")

        message = get_flashed_messages(category_filter="warning")
        assert result is None and message[0] == "nessun evento trovato"


def test_ricerca_evento_1_5_2(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')

        result = ricerca_eventi_per_categoria("gara di ballo")

        message = get_flashed_messages(category_filter="error")
        assert len(result)==0  and message[0] == "La categoria non esiste"

def test_ricerca_evento_1_5_3(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')

        result = ricerca_eventi_per_regione("Francia")

        message = get_flashed_messages(category_filter="error")
        assert len(result)==0  and message[0] == "La regione non esiste"

def test_ricerca_evento_1_5_4(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')

        result = ricerca_eventi_per_prezzo("-30","20")


        message = get_flashed_messages(category_filter="error")
        assert len(result) == 0 and message[0] == "il prezzo minore o massimo è negativo"













def test_ricerca_evento_1_5_5(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')

        result = ricerca_eventi_per_parola("sera")

        message = get_flashed_messages(category_filter="success")
        assert len(result) != 0  and message[0] == "evento trovato"


def test_ricerca_evento_1_5_6(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')

        result= ricerca_eventi_per_categoria("Conferenze e Seminari")

        message = get_flashed_messages(category_filter="success")
        assert result != None and message[0] == "La categoria esiste"




def test_ricerca_evento_1_5_7(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')

        result= ricerca_eventi_per_regione("Campania")

        message = get_flashed_messages(category_filter="success")
        assert result != None and message[0] == "La regione esiste"





def test_ricerca_evento_1_5_8(mock_app, ):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')

        result = ricerca_eventi_per_prezzo("30", "20")

        message = get_flashed_messages(category_filter="success")
        assert result != None and message[0] == "il prezzo minore o massimo non è negativo"
