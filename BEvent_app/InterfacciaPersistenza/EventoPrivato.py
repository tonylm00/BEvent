from .Evento import Evento


class Evento_Privato(Evento):
    def __init__(self, evento_data, evento_privato_data):
        super().__init__(evento_data)
        evento_info = evento_privato_data['EventoPrivato']
        self.festeggiato = evento_info['Festeggiato/i']
