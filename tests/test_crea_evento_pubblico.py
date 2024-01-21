from unittest.mock import patch, MagicMock
from flask import get_flashed_messages
from BEvent_app.GestioneEvento.GestioneEventoService import crea_evento_pubblico
from mock import mock_app

def test_crea_evento_pubblico(mock_app):

        with mock_app.app_context(), mock_app.test_client() as test_client:
            test_client.get('/mock_login_fornitore')
            with test_client.session_transaction() as sess:
                user_id = sess['id']
                result= crea_evento_pubblico("1949-4-20", "100", "Descrizione evento", b'immagine_binaria_dummy',
                                     "pubblico", "concerto", False, user_id, [],
                                         "20.00", "18:00", "Concerto Live", "Via della Musica, 123", "Lazio", "fake_id")

        result = get_dettagli_evento("6585c70d8e551a0d24352c2f")

