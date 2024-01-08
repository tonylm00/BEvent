from .Utente import Utente
from ..db import get_db
from ..Utils import Image

class Fornitore(Utente):
    def __init__(self, user_data, fornitore_data):
        super().__init__(user_data)
        fornitore_info = fornitore_data['Fornitore']
        self.descrizione = fornitore_info['Descrizione']
        self.eventi_max_giornalieri = fornitore_info['EventiMassimiGiornaliero']
        self.orario_lavoro = fornitore_info['OrarioDiLavoro']

        self.foto = []  # Inizializza un elenco vuoto per le immagini

        for foto_base64 in fornitore_info['Foto']:
            try:
                immagine = Image.convert_byte_array_to_image(foto_base64)
                self.foto.append(immagine)
            except Exception as e:
                print(f"Errore nella conversione dell'array di byte in immagine: {str(e)}")
        self.isCurrentVersion = True,
        self.isDeleted = False,
        self.citta = fornitore_info['Citta']
        self.via = fornitore_info['Via']
        self.p_Iva = fornitore_info['Partita_Iva']
        self.isLocation = fornitore_info['isLocation']

