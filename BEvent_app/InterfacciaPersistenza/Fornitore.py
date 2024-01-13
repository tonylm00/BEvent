import smtplib
from ..Utils.Observer import Observer
from . import Evento
from .Utente import Utente
from ..Utils import Image




class Fornitore(Utente,Observer):

    def __init__(self, user_data, fornitore_data):
        Utente.__init__(self, user_data)
        Observer.__init__(self)
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

        self.citta = fornitore_info['Citta']
        self.via = fornitore_info['Via']
        self.p_Iva = fornitore_info['Partita_Iva']
        self.isLocation = fornitore_info['isLocation']

    def update(self, observable):
        if isinstance(observable, Evento):
            messaggio = "L'evento in data " + observable.data + " è stato annullato!"
            email = smtplib.SMTP("smtp.gmail.com", 587)
            email.ehlo()
            email.starttls()
            email.login("beventc13@gmail.com", "Bevent1234.")
            email.sendmail("beventc13@gmail.com", self.email, messaggio)
            email.quit()