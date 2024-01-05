from ..Utils import Image
class Servizio_Offerto:
    def __init__(self, service_data):
        self._id = str(service_data['_id'])
        self.descrizione = service_data['Descrizione']
        self.tipo = service_data['Tipo']
        self.prezzo = service_data['Prezzo']
        self.quantita = service_data['Quantità']
        array_byte = service_data['FotoServizo']
        immagini = Image.convert_byte_array_to_image(array_byte)
        self.foto_servizio = immagini
        self.fornitore_associato = service_data['fornitore_associato']
