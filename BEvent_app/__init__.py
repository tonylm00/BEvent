from bson import ObjectId
from flask import Flask, render_template, request, session
from flask_login import LoginManager
from pymongo import MongoClient
from BEvent_app.Routes import home, login_page
from .InterfacciaPersistenza.Utente import Utente
from .Routes import views
from .db import get_db
from .Autenticazione.AutenticazioneController import aut
from .GestioneEvento.GestioneEventoController import ge
from .Fornitori.FornitoriController import Fornitori


def create_app():
    app = Flask(__name__)

    app.secret_key = 'BEvent'  # comando per impostare una password alle session, altrimenti non funziona

    app.config['SECRET_KEY'] = "BEVENT"
    datab = get_db()
    login_manager = LoginManager(app)

    app.register_blueprint(Fornitori, url_prefix="/")
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(aut, url_prefix='/')
    app.register_blueprint(ge, url_prefix='/')

    @login_manager.user_loader
    def load_user(user_id):
        # Converti user_id in ObjectId prima della query
        user_data = datab.utenti.find_one({'_id': ObjectId(user_id)})

        # Gestisci il caso in cui user_data è None
        if user_data:
            # Crea un'istanza della classe Utente con i dati recuperati
            return Utente(user_data)
        else:
            return None

    @app.route('/')
    def index():
        return home()

    return app
