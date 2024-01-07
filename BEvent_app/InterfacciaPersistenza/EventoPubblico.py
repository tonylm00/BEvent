from .Evento import Evento


class Evento_Pubblico(Evento):
    def __init__(self, evento_data, evento_pubblico_data):
        super().__init__(evento_data)
        evento_info = evento_pubblico_data['EventoPubblico']
        self.prezzo = evento_info['Prezzo']
