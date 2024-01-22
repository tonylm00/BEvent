from flask import get_flashed_messages
from BEvent_app.FeedBack.FeedBackService import inserisci_recensione
from mock import mock_app, mock_id_servizio


def test_inserisci_recensione_1_4_1(mock_app, mock_id_servizio):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = inserisci_recensione(mock_id_servizio, user_id, "5", "Un'esperienza indimenticabile!",
                                          "Un'esperienza straordinaria! Il servizio impeccabile si combina con "
                                          "un'atmosfera accogliente. I piatti deliziosi e creativi soddisfano ogni "
                                          "palato. Un vero gioiello culinario da non perdere")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "La descrizione della recensione è troppo lunga! "


def test_inserisci_recensione_1_4_2(mock_app, mock_id_servizio):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = inserisci_recensione(mock_id_servizio, user_id, "8", "Un'esperienza indimenticabile!",
                                          "Un'esperienza straordinaria! Il servizio impeccabile si combina con "
                                          "un'atmosfera accogliente. I piatti deliziosi e creativi soddisfano ogni "
                                          "palato.")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "Il voto non è un numero che va da 0 a 5 "


def test_inserisci_recensione_1_4_3(mock_app, mock_id_servizio):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = inserisci_recensione(mock_id_servizio, user_id, "5",
                                          "Un'esperienza indimenticabile con vista mozzafiato"
                                          "una struttura con vista piscina mozzafiato",
                                          "Un'esperienza straordinaria! Il servizio impeccabile si combina con "
                                          "un'atmosfera accogliente. I piatti deliziosi e creativi soddisfano ogni "
                                          "palato.")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "Il titolo della recensione è troppo lungo!"


def test_inserisci_recensione_1_4_4(mock_app, mock_id_servizio):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_organizzatore')
        with test_client.session_transaction() as sess:
            user_id = sess['id']
            result = inserisci_recensione(mock_id_servizio, user_id, "5", "Un'esperienza indimenticabile!",
                                          "Un'esperienza straordinaria! Il servizio impeccabile si combina con "
                                          "un'atmosfera accogliente. I piatti deliziosi e creativi soddisfano ogni "
                                          "palato. ")
            message = get_flashed_messages(category_filter="success")
            assert result is True and message[0] == "La recensione è stata scritta con successo!"
