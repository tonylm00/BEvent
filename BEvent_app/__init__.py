from flask import Flask, render_template, request
from BEvent_app.Routes import home, login_page
from .Routes import views
from .Autenticazione.AutenticazioneController import aut
from .Fornitori.FornitoriController import Fornitori

def create_app():
    app = Flask(__name__)
    app.secret_key = 'password'  # comando per impostare una password alle session, altrimenti non funziona
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(aut, url_prefix='/')
    app.register_blueprint(Fornitori,url_prefix='/')

    @app.route('/')
    def index():
        return home()

    return app
