from flask import get_flashed_messages

from BEvent_app.GestioneEvento.GestioneEventoService import save_evento
from mock import mock_app, mock_lista_fornitori, mock_lista_servizi


def test_save_evento_1_2_1(mock_app, mock_lista_fornitori, mock_lista_servizi):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = save_evento(mock_lista_servizi, mock_lista_fornitori, "Matrimonio2023", "20-12-2025",
                                 "56", "Antonio&Daria", "testcase", True, "2",
                                 "", "1234", user_id)

            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "Il tipo di evento non rispetta il formato previsto"


def test_save_evento_1_2_2(mock_app, mock_lista_fornitori, mock_lista_servizi):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = save_evento(mock_lista_servizi, mock_lista_fornitori, "Matrimonio", "2025-12-20",
                                 "56", "Antonio&Daria", "testcase", True, "2",
                                 "", "1234", user_id)
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "Formato data non corretto. Utilizzare il formato dd-mm-yyyy."


def test_save_evento_1_2_3(mock_app, mock_lista_fornitori, mock_lista_servizi):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = save_evento(mock_lista_servizi, mock_lista_fornitori, "Matrimonio", "20-12-2019",
                                 "56", "Antonio&Daria", "testcase", True, "2",
                                 "", "1234", user_id)
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "La data non è valida poichè è precedente alla data odierna."


def test_save_evento_1_2_4(mock_app, mock_lista_fornitori, mock_lista_servizi):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = save_evento(mock_lista_servizi, mock_lista_fornitori, "Matrimonio", "20-12-2025",
                                 "56 invitati", "Antonio&Daria", "testcase", True, "2",
                                 "", "1234", user_id)
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "Il numero di invitati non rispetta il formato previsto"


def test_save_evento_1_2_5(mock_app, mock_lista_fornitori, mock_lista_servizi):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = save_evento(mock_lista_servizi, mock_lista_fornitori, "Matrimonio", "20-12-2025",
                                 "56", "Antonio&Daria", "testcase", True, "2",
                                 "", "1234", user_id)
            message = get_flashed_messages(category_filter="success")
            assert result is True and message[0] == "L'evento è stato creato correttamente"
