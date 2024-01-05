import base64

from ..Utils import Image
class Servizio_Offerto:
    def __init__(self, service_data):
        self._id = str(service_data['_id'])
        self.descrizione = service_data['Descrizione']
        self.tipo = service_data['Tipo']
        self.prezzo = service_data['Prezzo']
        self.quantita = service_data['Quantità']
        self.foto_servizio = []  # Inizializza un elenco vuoto per le immagini

        for foto_base64 in service_data['FotoServizio']:
            try:
                immagine = Image.convert_byte_array_to_image(foto_base64)
                self.foto_servizio.append(immagine)
            except Exception as e:
                print(f"Errore nella conversione dell'array di byte in immagine: {str(e)}")

        self.fornitore_associato = service_data['fornitore_associato']
