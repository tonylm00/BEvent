from datetime import datetime
from ..db import get_db


def is_valid_data(data):
    try:
        datetime_data = datetime.strptime(data, '%d-%m-%Y')
        data_odierna = datetime.now().strftime('%d-%m-%Y')

        if datetime_data > datetime.strptime(data_odierna, '%d-%m-%Y'):
            return True
        else:
            return False

    except ValueError:
        return False


def get_fornitori():
    db = get_db()
    fornitori_collection = db['Utente']
    fornitori = list(fornitori_collection.find({'Ruolo': '3'}))
    return fornitori


def get_fornitori_by_tipo(tipo_desiderato):
    fornitori = get_fornitori()
    fornitori_filtrati = [fornitore for fornitore in fornitori if
                          fornitore.get("Fornitore", {}).get("Tipo") == tipo_desiderato]
    return fornitori_filtrati
