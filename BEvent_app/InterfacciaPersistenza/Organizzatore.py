from .Utente import Utente


class Organizzatore(Utente):
    """
        Classe che rappresenta un organizzatore, derivata dalla classe base Utente.

        Args:
            user_data (dict): Dati comuni a tutti gli utenti.
            organizzatore_data (dict): Dati specifici degli organizzatori.

        Attributi:
            citta (str): Città di residenza dell'organizzatore.
        """
    def __init__(self, user_data, organizzatore_data):
        """
                Inizializza un nuovo oggetto Organizzatore.

                Args:
                    user_data (dict): Dati comuni a tutti gli utenti.
                    organizzatore_data (dict): Dati specifici degli organizzatori.
                """
        super().__init__(user_data)
        organizzatore_info = organizzatore_data['Organizzatore']
        self.citta = organizzatore_info['Citta']
