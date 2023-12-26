from flask import request
from BEvent_app.Autenticazione import AutenticazioneService

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = AutenticazioneService.verify_user(email, password)

        if user:
            # Autenticazione riuscita
            return "Login riuscito!"
        else:
            return "Credenziali non valide. Riprova."
    else:
        return "Metodo non consentito per l'accesso."
