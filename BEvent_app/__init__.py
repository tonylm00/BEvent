from bson import ObjectId
from flask import Flask
from flask_login import LoginManager
from BEvent_app.Routes import home
from .InterfacciaPersistenza.Fornitore import Fornitore
from .InterfacciaPersistenza.Organizzatore import Organizzatore
from .InterfacciaPersistenza.Utente import Utente
from .Routes import views
from .db import get_db
from .Autenticazione.AutenticazioneController import aut
from .GestioneEvento.GestioneEventoController import ge
from .Fornitori.FornitoriController import Fornitori
from .RicercaEvento.RicercaEventoController import re
from .FeedBack.FeedBackController import fb


def create_app():
    app = Flask(__name__)

    app.secret_key = 'BEvent'  # comando per impostare una password alle session, altrimenti non funziona

    app.config['SECRET_KEY'] = "BEVENT"
    datab = get_db()
    login_manager = LoginManager(app)
    login_manager.login_view = 'views.home'

    app.register_blueprint(Fornitori, url_prefix="/")
    app.register_blueprint(fb, url_prefix="/")
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(aut, url_prefix='/')
    app.register_blueprint(ge, url_prefix='/')
    app.register_blueprint(re, url_prefix='/')

    def get_user_by_id(user_id):
        user_data = datab.Utente.find_one({'_id': ObjectId(user_id)})

        if user_data:
            if user_data['Ruolo'] == '2':
                return Organizzatore(user_data, user_data)
            elif user_data['Ruolo'] == '3':
                return Fornitore(user_data, user_data)

        return None

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)

    @app.route('/')
    def index():
        return home()

    return app
