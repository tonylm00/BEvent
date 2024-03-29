from unittest.mock import MagicMock

import pytest
from bson import ObjectId
from flask import session
from flask_login import login_user, current_user

from BEvent_app import create_app
from BEvent_app.InterfacciaPersistenza.Fornitore import Fornitore
from BEvent_app.InterfacciaPersistenza.Organizzatore import Organizzatore
from BEvent_app.InterfacciaPersistenza.ServizioOfferto import ServizioOfferto
from BEvent_app.Routes import views
from db import get_db

# Mocking GestioneEventoService functions
GestioneEventoService = MagicMock()

db = get_db()


@views.route('/mock_login_organizzatore')
def mock_login_organizzatore():
    user_data = {
        "_id": "65a958fc1423cc09d49a4c75",
        "nome": "Angelo",
        "cognome": "De Luca",
        "data_di_nascita": "23-05-2002",
        "email": "adl@gmail.com",
        "telefono": "0123456789",
        "nome_utente": "hanstarz",
        "password": "pbkdf2:sha256"
                    ":600000$KUILXMDssMxmvug8$6530c694d0a82d56b896c721bd56ca929a0343d18fb127f830a0c86de2a5fd60",
        "Admin": {
            "isAdmin": False
        },
        "Ruolo": "2",
        "regione": "Campania",
        "Organizzatore": {
            "Citta": "Caserta"
        }
    }

    organizzatore = Organizzatore(user_data, user_data)

    if not db.Utente.find_one({"email": user_data["email"]}):
        db.Utente.insert_one(user_data)

    login_user(organizzatore)
    session['id'] = organizzatore.id
    session['ruolo'] = organizzatore.ruolo
    session['nome_utente'] = organizzatore.nome_utente
    session['regione'] = organizzatore.regione

    return "organizzatore loggato"


@views.route('/mock_login_fornitore')
def mock_login_fornitore():
    user_data = {
        "_id": {
            "$oid": "65a956b7c4e2c6f986e1e54f"
        },
        "nome": "Teresa",
        "cognome": "Rossi",
        "data_di_nascita": "12-12-1984",
        "email": "trossi@gmail.com",
        "telefono": "0123456789",
        "nome_utente": "Trattoria Da Teresa",
        "password": "pbkdf2:sha256"
                    ":600000$L7CnBoPe9odp356G$2926549e372d6263a32077be925398b59ca8ac107582cda51bfdb0564f3b4959",
        "Admin": {
            "isAdmin": False
        },
        "Ruolo": "3",
        "regione": "Campania",
        "Fornitore": {
            "Descrizione": "Trattoria elegante con spazio all'aperto e piscina",
            "EventiMassimiGiornaliero": "2",
            "OrarioDiLavoro": "",
            "Foto": [],
            "Citta": "Caserta",
            "Via": "Via Vigna Brigida",
            "Partita_Iva": "01234567890",
            "isLocation": True
        }
    }

    fornitore = Fornitore(user_data, user_data)

    if not db.Utente.find_one({"email": user_data["email"]}):
        db.Utente.insert_one(user_data)

    login_user(fornitore)
    session['id'] = current_user.get_id()
    session['ruolo'] = fornitore.ruolo
    session['nome_utente'] = fornitore.nome_utente
    session['regione'] = fornitore.regione
    session['is_location'] = fornitore.isLocation

    return "Fornitore loggato"


@pytest.fixture
def mock_app():
    app = create_app()
    app.testing = True

    return app


@pytest.fixture
def mock_lista_fornitori():
    fornitori_id = [ObjectId("65a9553dc4e2c6f986e1e53d"), ObjectId("65a956b7c4e2c6f986e1e54f")]
    fornitori_data = db.Utente.find({'_id': {"$in": fornitori_id}})
    lista_fornitori = []
    for data in fornitori_data:
        fornitore = Fornitore(data, data)
        lista_fornitori.append(fornitore)

    return lista_fornitori


@pytest.fixture
def mock_lista_servizi():
    servizi_id = [ObjectId("65a955adc4e2c6f986e1e543"), ObjectId("65a95714c4e2c6f986e1e555")]
    servizi_data = db['Servizio Offerto'].find({'_id': {"$in": servizi_id}})
    lista_servizi = []
    for data in servizi_data:
        servizio = ServizioOfferto(data)
        lista_servizi.append(servizio)

    return lista_servizi


@pytest.fixture
def mock_id_servizio():
    servizio_data = db['Servizio Offerto'].find_one({'_id': ObjectId('65abf12b28b8c19ea42ad49b')})
    servizio_id = servizio_data['_id']
    return servizio_id


def get_dettagli_evento():
    return {'id': 1, 'name': 'Evento'}


def get_dati_organizzatore():
    return {'organizer_id': 123, 'organizer_name': 'Organizzatore'}


def get_dati_servizi_organizzatore():
    return [{'service_id': 456, 'service_name': 'Servizio'}]


GestioneEventoService.get_dettagli_evento.side_effect = get_dettagli_evento
GestioneEventoService.get_dati_organizzatore.side_effect = get_dati_organizzatore
GestioneEventoService.get_dati_servizi_organizzatore.side_effect = get_dati_servizi_organizzatore
