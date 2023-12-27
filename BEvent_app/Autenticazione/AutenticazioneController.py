from flask import request, Flask, Blueprint
from BEvent_app.Autenticazione import AutenticazioneService
from BEvent_app.Autenticazione.AutenticazioneService import ruolo


app = Flask(__name__)
aut = Blueprint('aut', __name__)

def login():
    print("hellooooo")
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
        data_di_nascita = request.form.get('data_di_nascita')
        nome_utente = request.form.get('nome_utente')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        telefono = request.form.get('telefono')
        isAdmin = request.form.get('isAdmin')
        ruolo = request.form.get('ruolo')
        if registra_utente(nome,cognome,data_di_nascita,nome_utente,email,password,cpassword,telefono,isAdmin,ruolo):
            return home()
    return registrazione_page()

