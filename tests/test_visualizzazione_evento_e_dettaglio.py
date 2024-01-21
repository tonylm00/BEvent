
from flask import get_flashed_messages

from BEvent_app.Fornitori.FornitoriService import get_dettagli_evento, get_dati_organizzatore,get_dati_servizi
from mock import mock_app

def test_get_dettagli_evento(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_fornitore')

        result=get_dettagli_evento("luci")

        message = get_flashed_messages(category_filter="warning")
        assert result is None and message[0] == "ok"