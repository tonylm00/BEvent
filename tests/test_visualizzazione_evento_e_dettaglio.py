import unittest
from BEvent_app.GestioneEvento.GestioneEventoController import visualizza_evento_dettagli_controller
from mocks import GestioneEventoService

class TestGestioneEventoController(unittest.TestCase):

    def test_visualizza_evento_dettagli_controller(self):

        request_form = {'id': '1'}
        expected_evento = {'id': 1, 'name': 'Evento'}
        expected_organizzatore = {'organizer_id': 123, 'organizer_name': 'Organizzatore'}
        expected_servizi = [{'service_id': 456, 'service_name': 'Servizio'}]


        with patch('BEvent_app.GestioneEvento.GestioneEventoController.request', request_form), \
             patch('BEvent_app.GestioneEvento.GestioneEventoController.GestioneEventoService', GestioneEventoService):
            response = visualizza_evento_dettagli_controller()


        GestioneEventoService.get_dettagli_evento.assert_called_once_with('1')
        GestioneEventoService.get_dati_organizzatore.assert_called_once_with('1')
        GestioneEventoService.get_dati_servizi_organizzatore.assert_called_once_with('1')

        self.assertEqual(response.evento, expected_evento)
        self.assertEqual(response.organizzatore, expected_organizzatore)
        self.assertEqual(response.servizi, expected_servizi)

if __name__ == '__main__':
    unittest.main()
