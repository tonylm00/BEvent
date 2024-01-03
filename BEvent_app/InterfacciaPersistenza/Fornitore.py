from .Utente import Utente


class Fornitore(Utente):
    def __init__(self, user_data, fornitore_data):
        super().__init__(user_data)
        fornitore_info = fornitore_data['Fornitore']
        self.descrizione = fornitore_info['Descrizione']
        self.eventi_max_giornalieri = fornitore_info['EventiMassimiGiornaliero']
        self.orario_lavoro = fornitore_info['OrarioDiLavoro']
        self.quantita = fornitore_info['Quantità']
        self.foto = fornitore_info['Foto']
        self.citta = fornitore_info['Citta']
        self.via = fornitore_info['Via']
        self.p_Iva = fornitore_info['Partita_Iva']
        self.isLocation = fornitore_info['isLocation']
