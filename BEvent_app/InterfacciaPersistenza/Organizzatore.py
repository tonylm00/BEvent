from .Utente import Utente


class Organizzatore(Utente):
    def __init__(self, user_data, organizzatore_data):
        super().__init__(user_data)
        self.foto = organizzatore_data['FotoOrganizzatore']
        self.citta = organizzatore_data['Citta']

