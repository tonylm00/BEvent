from .Utente import Utente


class Admin(Utente):
    def __init__(self, user_data):
        super().__init__(user_data)
        self.isAdmin = True
