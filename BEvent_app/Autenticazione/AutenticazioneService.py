import hashlib
from pymongo import MongoClient, collection
from BEvent_app.Routes import ruolo_utente

# import hashlib

client = MongoClient('mongodb://localhost:27017/')
db = client['BEvent']
users_collection = db['Utente']


#def hash_password(password):
#    return hashlib.sha256(password.encode()).hexdigest()


def verify_user(email, password):
    user = users_collection.find_one({'email': email, 'password': password})
    return user


def ruolo(email):
    user = users_collection.find_one({'email': email})
    if user:
        ruolo = user.get('ruolo', None)
        return ruolo
    return None
