from .Evento import Evento


class EventoPrivato(Evento):
    """
       Classe che rappresenta un evento privato, derivata dalla classe base Evento.

       Args:
           evento_data (dict): Dati dell'evento comuni a tutti gli eventi.
           evento_privato_data (dict): Dati specifici degli eventi privati.

       Attributi:
           festeggiato (str): Nome del festeggiato o festeggiati.
           prezzo (float): Prezzo dell'evento privato.
           organizzatore (str): Nome dell'organizzatore dell'evento privato.
       """
    def __init__(self, evento_data, evento_privato_data):
        """
               Inizializza un nuovo oggetto EventoPrivato.

               Args:
                   evento_data (dict): Dati dell'evento comuni a tutti gli eventi.
                   evento_privato_data (dict): Dati specifici degli eventi privati.
               """
        super().__init__(evento_data)
        evento_info = evento_privato_data['EventoPrivato']
        self.festeggiato = evento_info['Festeggiato/i']
        self.prezzo = evento_info['Prezzo']
        self.organizzatore = evento_info['Organizzatore']
