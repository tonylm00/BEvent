from flask import Flask, render_template, request
from BEvent_app.Routes import home, login_page
import hashlib



def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return home()

    return app
