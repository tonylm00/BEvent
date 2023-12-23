from flask import Flask, render_template, request
from pymongo import MongoClient
import hashlib

client = MongoClient('mongodb://localhost:27017/')
db = client['BEvent']
users_collection = db['Utente']


def create_app():
    app = Flask(__name__, static_folder='static')

    @app.route('/')
    def index():
        return render_template('Login.html')

    @app.route('/login', methods=['POST'])
    def login():
        email = request.form.get('email')
        password = request.form.get('password')

        user = users_collection.find_one({'email': email, 'password': password})
        if user:
            return "Login riuscito!"
        else:
            return "Credenziali non valide. Riprova."

    return app
