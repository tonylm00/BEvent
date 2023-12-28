from .Utente import Utente


class Fornitore(Utente):
    def __init__(self, user_data, fornitore_data):
        super().__init__(user_data)
        self.descrizione = fornitore_data['Descrizione']
        self.tipo = fornitore_data['Tipo']
        self.prezzo = fornitore_data['Prezzo']
        self.eventi_max_giornalieri = fornitore_data['EventiMassimiGiornaliero']
        self.orario_lavoro = fornitore_data['OrarioDiLavoro']
        self.quantita = fornitore_data['Quantità']
        self.foto = fornitore_data['Foto']
        self.citta = fornitore_data['Citta']
        self.via = fornitore_data['Via']
        self.p_Iva = fornitore_data['Partita_Iva']
