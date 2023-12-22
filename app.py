from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import hashlib

app = Flask(__name__, static_folder='style')
client = MongoClient('mongodb://localhost:27017/')
db = client['BEvent']
users_collection = db['Utente']


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    #hashed_password = hash_password(password)  # Crittografia della password


    #user = users_collection.find_one({'email': email, 'password': hashed_password})

    user = users_collection.find_one({'email': email, 'password': password})
    if user:
        # Autenticazione riuscita
        return "Login riuscito!"
    else:

        return "Credenziali non valide. Riprova."

if __name__ == '__main__':
    app.run(debug=True)