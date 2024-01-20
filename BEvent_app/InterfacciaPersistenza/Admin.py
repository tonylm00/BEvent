from .Utente import Utente

class Admin(Utente):
    """
       Classe che rappresenta un utente con privilegi di amministratore, derivata dalla classe base Utente.

       Args:
           user_data (dict): Dati dell'utente comuni a tutti gli utenti.

       Attributi:
           isAdmin (bool): Indica se l'utente ha privilegi di amministratore.
       """
    def __init__(self, user_data):
        """
               Inizializza un nuovo oggetto Admin.

               Args:
                   user_data (dict): Dati dell'utente comuni a tutti gli utenti.
               """
        super().__init__(user_data)
        self.isAdmin = True
