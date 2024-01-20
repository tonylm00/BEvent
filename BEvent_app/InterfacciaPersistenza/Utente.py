from flask_login import UserMixin
from werkzeug.security import check_password_hash


class Utente(UserMixin):
    """
       Classe che rappresenta un utente.

       Args:
           user_data (dict): Dati dell'utente.

       Attributi:
           id (str): Identificatore univoco dell'utente.
           nome (str): Nome dell'utente.
           cognome (str): Cognome dell'utente.
           data_nascita (str): Data di nascita dell'utente.
           email (str): Indirizzo email dell'utente.
           telefono (str): Numero di telefono dell'utente.
           nome_utente (str): Nome utente dell'utente.
           password_hash (str): Hash della password dell'utente.
           ruolo (str): Ruolo dell'utente.
           regione (str): Regione di residenza dell'utente.
           isAdmin (bool): Indica se l'utente ha privilegi di amministratore.
       """
    def __init__(self, user_data):
        """
                Inizializza un nuovo oggetto Utente.

                Args:
                    user_data (dict): Dati dell'utente.
                """
        self.id = str(user_data['_id'])
        self.nome = user_data['nome']
        self.cognome = user_data['cognome']
        self.data_nascita = user_data['data_di_nascita']
        self.email = user_data['email']
        self.telefono = user_data['telefono']
        self.nome_utente = user_data['nome_utente']
        self.password_hash = user_data['password']
        self.ruolo = user_data['Ruolo']
        self.regione = user_data['regione']
        self.isAdmin = False

    def get_id(self):
        """
               Restituisce l'identificatore univoco dell'utente.

               Returns:
                   str: Identificatore univoco dell'utente.
               """
        return str(self.id)

    def check_password(self, password):
        """
               Verifica se la password fornita corrisponde alla password dell'utente.

               Args:
                   password (str): Password da verificare.

               Returns:
                   bool: True se la password è corretta, False altrimenti.
               """

        return check_password_hash(self.password_hash, password)
