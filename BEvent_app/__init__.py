from flask import Flask, render_template, request
from BEvent_app.Routes import home, login_page, user_page
from .Routes import views
from .Autenticazione.AutenticazioneController import aut


def create_app():
    app = Flask(__name__)
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(aut, url_prefix='/')
    @app.route('/')
    def index():
        return login_page()

    return app
