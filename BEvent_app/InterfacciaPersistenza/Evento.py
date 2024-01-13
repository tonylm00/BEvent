from ..Utils import Image


class Evento:
    def __init__(self, evento_data):
        self.id = str(evento_data['_id'])
        self.data = evento_data['Data']
        self.n_persone = evento_data['Invitati/Posti']
        self.descrizione = evento_data['Descrizione']

        if evento_data.get('Locandina'):
            try:
                self.locandina = Image.convert_byte_array_to_image(evento_data['Locandina'])
            except Exception as e:
                print(f"Errore nella conversione del bytearray in immagine: {str(e)}")
                self.locandina = None
        else:
            self.locandina = None

        self.ruolo = evento_data['Ruolo']
        self.tipo = evento_data['Tipo']
        self.isPagato = bool(evento_data['isPagato'])
        self.fornitori_associati = evento_data.get('fornitori_associati', [])
        self.observers=self.fornitori_associati
        self.servizi_associati = evento_data.get('servizi_associati', [])
