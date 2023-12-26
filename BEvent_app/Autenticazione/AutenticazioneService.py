from pymongo import MongoClient
import hashlib

client = MongoClient('mongodb://localhost:27017/')
db = client['BEvent']
users_collection = db['Utente']

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(email, password):
    user = users_collection.find_one({'email': email, 'password': hash_password(password)})
    return user
