from .Utente import Utente



class Organizzatore(Utente):
    def __init__(self, user_data, organizzatore_data):
        super().__init__(user_data)
        organizzatore_info = organizzatore_data['Organizzatore']
        self.foto = organizzatore_info['FotoOrganizzatore']
        self.citta = organizzatore_info['Citta']

