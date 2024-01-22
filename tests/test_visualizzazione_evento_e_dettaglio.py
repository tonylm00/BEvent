import unittest
from unittest.mock import patch, MagicMock

from bson.objectid import ObjectId
from flask import Flask, template_rendered

# Import the necessary modules or objects from your application
from BEvent_app.GestioneEvento.GestioneEventoController import visualizza_evento_dettagli_controller


# Context manager to capture templates and their contexts
class CaptureTemplateRenderedContext():
    def __init__(self):
        self.templates = []

    def __enter__(self):
        template_rendered.connect(self.record)

    def __exit__(self, exc_type, exc_value, traceback):
        template_rendered.disconnect(self.record)

    def record(self, sender, template, context, **extra):
        self.templates.append((template, context))


class TestVisualizzaEventoDettagliController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('BEvent_app.GestioneEvento.GestioneEventoController.get_dettagli_evento')
    @patch('BEvent_app.GestioneEvento.GestioneEventoController.get_dati_organizzatore')
    @patch('BEvent_app.GestioneEvento.GestioneEventoService.get_dati_servizi_organizzatore')
    @patch('BEvent_app.GestioneEvento.GestioneEventoController.get_db')
    def test_visualizza_evento_dettagli_controller(self, mock_get_db, mock_get_dati_servizi_organizzatore,
                                                   mock_get_dati_organizzatore, mock_get_dettagli_evento):
        # Arrange
        mock_evento = MagicMock()
        mock_organizzatore = MagicMock()
        mock_servizi = [MagicMock(), MagicMock()]

        mock_get_dettagli_evento.return_value = mock_evento
        mock_get_dati_organizzatore.return_value = mock_organizzatore
        mock_get_dati_servizi_organizzatore.return_value = mock_servizi
        mock_get_db.return_value = MagicMock()

        # To simulate the ObjectId, since it's used in your query
        mock_event_id = ObjectId()

        # Act
        with CaptureTemplateRenderedContext() as ctx:
            with self.app.test_request_context('/Visuallizza_Dettagli_evento_Organizzatore',
                                               method='POST',
                                               data={'id': str(mock_event_id)}):
                response = visualizza_evento_dettagli_controller()

        # Assert
        self.assertEqual(response.status_code, 200)
        mock_get_dettagli_evento.assert_called_once_with(str(mock_event_id))
        mock_get_dati_organizzatore.assert_called_once_with(str(mock_event_id))
        mock_get_dati_servizi_organizzatore.assert_called_once_with(str(mock_event_id))

        # Check that the correct template was rendered with the expected context variables
        template, context = ctx.templates[0]
        self.assertEqual(template.name, 'dettagliEventoPrivato.html')
        self.assertDictContainsSubset(
            {'evento': mock_evento, 'organizzatore': mock_organizzatore, 'servizi': mock_servizi}, context)


if __name__ == '__main__':
    unittest.main()
