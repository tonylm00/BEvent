from unittest.mock import patch, MagicMock
from flask import get_flashed_messages
from BEvent_app.GestioneEvento.GestioneEventoService import crea_evento_pubblico
from mock import mock_app

def test_crea_evento_pubblico_1_3_1(mock_app):

        with mock_app.app_context(), mock_app.test_client() as test_client:
            test_client.get('/mock_login_fornitore')
            with test_client.session_transaction() as sess:
                user_id = sess['id']
                result = crea_evento_pubblico("10-10-1940","5","descrizione","",1,"Evento Sociale",False,[user_id],[],"500","20:00","nomeEvento","via via","Lazio",user_id)
                message = get_flashed_messages(category_filter="error")
                assert result is False and message[0] == "La data non è valida poichè è precedente alla data odierna."


def test_crea_evento_pubblico_1_3_2(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_fornitore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = crea_evento_pubblico("10-10-2024", "cinque", "descrizione", "", 1, "Evento Sociale", False,
                                          [user_id], [], "500", "20:00", "nomeEvento", "via via", "Lazio", user_id)
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "il numero di persone non è valido"

def test_crea_evento_pubblico_1_3_3(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_fornitore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = crea_evento_pubblico("10-10-2024", "5", "descrizione", "", 1, "Evento", False,
                                          [user_id], [], "500", "20:00", "nomeEvento", "via via", "Lazio", user_id)
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "il tipo di evento selezionato non è valido"

def test_crea_evento_pubblico_1_3_2(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_fornitore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = crea_evento_pubblico("10-10-2024", "5", "descrizione", "", 1, "Evento Sociale", False,
                                          [user_id], [], "cinquecento", "20:00", "nomeEvento", "via via", "Lazio", user_id)
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "il prezzo selezionato non è valido"

def test_crea_evento_pubblico_1_3_2(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_fornitore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = crea_evento_pubblico("10-10-2024", "5", "descrizione", "", 1, "Evento Sociale", False,
                                          [user_id], [], "500", "28:99", "nomeEvento", "via via", "Lazio", user_id)
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "il formato dell'ora non è valido"


def test_crea_evento_pubblico_1_3_2(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_fornitore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = crea_evento_pubblico("10-10-2024", "5", "descrizione", "", "1", "Evento Sociale", False,
                                          [user_id], [], "500", "13:00", "nomeEvento", "via via", "Lazio", user_id)

            message = get_flashed_messages(category_filter="success")
            assert result is True and message[0] == "l'evento è stato creato con successo!"