from .Evento import Evento


class Evento_Pubblico(Evento):
    def __init__(self, evento_data, evento_pubblico_data):
        super().__init__(evento_data)
        evento_info = evento_pubblico_data['EventoPubblico']
        self.prezzo = evento_info['Prezzo']
        self.nome = evento_info['Nome']
        self.regione = evento_info['Regione']
        self.luogo = evento_info['Luogo']
        self.ora = evento_info['Ora']

        self.biglietti_disponibili = evento_info['BigliettiDisponibili']

