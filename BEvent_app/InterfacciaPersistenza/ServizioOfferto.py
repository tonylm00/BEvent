
from ..Utils import Image


class ServizioOfferto:
    """
       Classe che rappresenta un servizio offerto.

       Args:
           service_data (dict): Dati del servizio offerto.

       Attributes:
           _id (str): Identificatore univoco del servizio.
           descrizione (str): Descrizione del servizio.
           tipo (str): Tipo del servizio.
           prezzo (float): Prezzo del servizio.
           foto_servizio (list): Elenco di immagini associate al servizio.
           isCurrentVersion (bool): Indica se il servizio è la versione corrente.
           isDeleted (bool): Indica se il servizio è stato eliminato.
           fornitore_associato (str): ID del fornitore associato al servizio.
       """
    def __init__(self, service_data):
        """
                Inizializza un nuovo oggetto ServizioOfferto.

                Args:
                    service_data (dict): Dati del servizio offerto.
                """
        self._id = str(service_data['_id'])
        self.descrizione = service_data['Descrizione']
        self.tipo = service_data['Tipo']
        self.prezzo = service_data['Prezzo']
        self.foto_servizio = []
        self.isCurrentVersion = service_data['isCurrentVersion'],
        self.isDeleted = service_data['isDeleted'],
        for foto_base64 in service_data['FotoServizio']:
            try:
                immagine = Image.convert_byte_array_to_image(foto_base64)
                self.foto_servizio.append(immagine)
            except Exception as e:
                print(f"Errore nella conversione dell'array di byte in immagine: {str(e)}")

        self.fornitore_associato = service_data['fornitore_associato']
