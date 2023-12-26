from flask import request
from BEvent_app.Autenticazione import AutenticazioneService
from BEvent_app.Autenticazione.AutenticazioneService import ruolo


def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = AutenticazioneService.verify_user(email, password)

        if user:
            # Autenticazione riuscita
            return ruolo(email)
        else:
            return "Credenziali non valide. Riprova."
    else:
        return "Metodo non consentito per l'accesso"


