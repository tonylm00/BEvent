from pymongo import MongoClient


def get_db():
    client = MongoClient("mongodb://localhost:27017/BEventTest")
    return client['BEventTest']
