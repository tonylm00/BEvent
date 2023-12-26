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

#@gu.route('/registrazione', methods=['GET','POST'])
def registrazione():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        nome_utente = request.form.get('nome_utente')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        telefono = request.form.get('telefono')
        indirizzo = request.form.get('indirizzo')
        tipo = request.form.get('tipo')
        if registra_utente(nome,cognome,nome_utente,email,password,cpassword,telefono,indirizzo,tipo):
            return home()
    return registrazione_page()

