from ..Fornitori.FornitoriService import get_fornitori
from ..Utils import Image
from ..Utils.Observable import Observable


class Evento(Observable):
    """
        Classe che rappresenta un evento osservabile.

        Args:
            evento_data (dict): Dati dell'evento.

        Attributi:
            id (str): Identificatore univoco dell'evento.
            data (str): Data dell'evento.
            n_persone (int): Numero di invitati o posti disponibili per l'evento.
            descrizione (str): Descrizione dell'evento.
            locandina (Image or None): Locandina dell'evento, convertita da un bytearray.
            ruolo (str): Ruolo dell'evento.
            tipo (str): Tipo dell'evento.
            isPagato (bool): Indica se l'evento è stato pagato.
            fornitori_associati (list): Lista di fornitori associati all'evento.
            servizi_associati (list): Lista di servizi associati all'evento.
        """
    def __init__(self, evento_data):
        """
               Inizializza un nuovo oggetto Evento.

               Args:
                   evento_data (dict): Dati dell'evento.
               """
        self.id = str(evento_data['_id'])
        self.data = evento_data['Data']
        self.n_persone = evento_data['Invitati/Posti']
        self.descrizione = evento_data['Descrizione']

        if evento_data.get('Locandina'):
            try:
                self.locandina = Image.convert_byte_array_to_image(evento_data['Locandina'])
            except Exception as e:
                messaggio = "Errore nella conversione del bytearray in immagine:" + str(e)
                print(messaggio)
                self.locandina = None
        else:
            self.locandina = None

        self.ruolo = evento_data['Ruolo']
        self.tipo = evento_data['Tipo']
        self.isPagato = bool(evento_data['isPagato'])
        self.fornitori_associati = evento_data.get('fornitori_associati', [])
        Observable.__init__(self, get_fornitori(self.fornitori_associati))
        self.servizi_associati = evento_data.get('servizi_associati', [])
