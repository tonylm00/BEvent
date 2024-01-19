from flask import get_flashed_messages
from BEvent_app.Autenticazione.AutenticazioneService import registra_forn
from mock import mock_app

def test_registra_forn_1_1_1(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Rossi","TRATTORIADATERESADICASERTAINVIABRIGIDA","rossit@gmail.com","Ciao.123",
                                   "Ciao.123","0123456789",
                                   "12-12-1984","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","01234567890","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="Nome Utente non valido"


def test_registra_forn_1_1_2(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Rossi","Trattoria da Terry","rossitgmail.com","Ciao.123",
                                   "Ciao.123","0123456789",
                                   "12-12-1984","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","01234567890","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="E-mail non valido"




def test_registra_forn_1_1_3(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Rossi","Trattoria da Terry","rossit@gmail.com","Ciao.3",
                                   "Ciao.3","0123456789",
                                   "1984-12-12","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","01234567890","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="Lunghezza non valida"


def test_registra_forn_1_1_4(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Rossi","Trattoria da Terry","rossit@gmail.com","ciao123ao",
                                   "ciao123ao","0123456789",
                                   "1984-12-12","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","01234567890","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="Formato non valido"


def test_registra_forn_1_1_5(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Rossi","Trattoria da Terry","rossit@gmail.com","Ciao.1234",
                                   "Ciao.123","0123456789",
                                   "1984-12-12","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20a","01234567890","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="Le password non corrispondono"


def test_registra_forn_1_1_6(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teres4","Rossi","Trattoria da Terry","rossit@gmail.com","Ciao.123",
                                   "Ciao.123","0123456789",
                                   "1984-12-12","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","01234567890","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="Nome non valido"


def test_registra_forn_1_1_7(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Ross1","Trattoria da Terry","rossit@gmail.com","Ciao.123",
                                   "Ciao.123","0123456789",
                                   "1984-12-12","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","01234567890","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="Cognome non valido"



def test_registra_forn_1_1_8(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Rossi","Trattoria da Terry","rossit@gmail.com","Ciao.123",
                                   "Ciao.123","zero",
                                   "1984-12-12","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","01234567890","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="Numero telefono non valido"

def test_registra_forn_1_1_9(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Rossi","Trattoria da Terry","rossit@gmail.com","Ciao.123",
                                   "Ciao.123","01234567890",
                                   "1984-12-12","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","01234567890","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="Numero telefono non valido"


def test_registra_forn_1_1_10(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Rossi","Trattoria da Terry","rossit@gmail.com","Ciao.123",
                                   "Ciao.123","0123456789",
                                   "12-12-2024","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","01234567890","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="Data di nascita non valida"


def test_registra_forn_1_1_11(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Rossi","Trattoria da Terry","rossit@gmail.com","Ciao.123",
                                   "Ciao.123","0123456789",
                                   "1984-12-12","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","012345678901","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="Partita iva non valida"

def test_registra_forn_1_1_12(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Rossi","Trattoria da Terry","rossit@gmail.com","Ciao.123",
                                   "Ciao.123","0123456789",
                                   "1984-12-12","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","zero","Campania")
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0]=="Partita iva non valida"


def test_registra_forn_1_1_13(mock_app):
    with mock_app.test_request_context():
        with mock_app.app_context():
            result = registra_forn("Teresa","Rossi","Trattoria da Terry","rossit@gmail.com","Ciao.123",
                                   "Ciao.123","0123456789",
                                   "1984-12-12","Caserta","3","Trattoria elegante con spazio all'aperto e piscina", True,"2",
                                   "Via Vigna Brigida 20","01234567890","Campania")
            message = get_flashed_messages(category_filter="success")
            assert result is True and message[0]=="Registrazione avvenuta con successo!"