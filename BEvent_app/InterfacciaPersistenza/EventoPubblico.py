from .Evento import Evento


class EventoPubblico(Evento):
    """
        Classe che rappresenta un evento pubblico, derivata dalla classe base Evento.

        Args:
            evento_data (dict): Dati dell'evento comuni a tutti gli eventi.
            evento_pubblico_data (dict): Dati specifici degli eventi pubblici.

        Attributi:
            prezzo (float): Prezzo dell'evento pubblico.
            nome (str): Nome dell'evento pubblico.
            regione (str): Regione in cui si svolge l'evento pubblico.
            luogo (str): Luogo dell'evento pubblico.
            ora (str): Ora in cui si svolge l'evento pubblico.
            biglietti_disponibili (int): Numero di biglietti disponibili per l'evento pubblico.
        """

    def __init__(self, evento_data, evento_pubblico_data):
        """
                Inizializza un nuovo oggetto EventoPubblico.

                Args:
                    evento_data (dict): Dati dell'evento comuni a tutti gli eventi.
                    evento_pubblico_data (dict): Dati specifici degli eventi pubblici.
                """
        super().__init__(evento_data)
        evento_info = evento_pubblico_data['EventoPubblico']
        self.prezzo = evento_info['Prezzo']
        self.nome = evento_info['Nome']
        self.regione = evento_info['Regione']
        self.luogo = evento_info['Luogo']
        self.ora = evento_info['Ora']

        self.biglietti_disponibili = evento_info['BigliettiDisponibili']

