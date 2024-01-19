from flask import get_flashed_messages
from BEvent_app.Fornitori.FornitoriService import aggiungi_servizio
from mock import mock_app

def test_aggiungi_servizio_1_6_1(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_fornitore')
        with test_client.session_transaction() as sess:
            forn = sess['id']
            servizio_data={
                "Descrizione" : "Benvenuti al Galactic Lounge per la serata Space Invaders! il ritorno di big Boss Le pareti illuminate da luci neon blu e viola, i cocktail come Galactic Nebula, i giochi retro come Space Invaders, e le competizioni di cosplay spaziale rendono l atmosfera unica. Performer acrobatici e giochi di luci culminano in un countdown spaziale da urlo, seguito da coriandoli assurdi omega e sempre stellari da favola, trasportandovi assurdo-omega in un viaggio maga-intergalattico di divertimento e fantascienza! Fenomenale. ",
                "Tipo": "Serata_Evento",
                "Quantità" : "2",
                "Prezzo" : 5000,
                "fornitore_associato" : forn,
                "isDeleted": False,
                "isCurrentVersion": None
            }
            result = aggiungi_servizio(servizio_data)
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "La descrizione non deve superare i 500 caratteri"
def test_aggiungi_servizio_1_6_2(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_fornitore')
        with test_client.session_transaction() as sess:
            forn = sess['id']
            servizio_data={
                "Descrizione" : "Benvenuti al Galactic Lounge per la serata Space Invaders! Le pareti illuminate da luci neon blu e viola, i cocktail come Galactic Nebula, i giochi retro come Space Invaders, e le competizioni di cosplay spaziale rendono l atmosfera unica. Performer acrobatici e giochi di luci culminano in un countdown spaziale da urlo, seguito da coriandoli assurdi omega e sempre stellari da favola, trasportandovi assurdo-omega in un viaggio maga-intergalattico di divertimento e fantascienza! Fenomenale. ",
                "Tipo": "Serata_Evento",
                "Quantità" : "2",
                "Prezzo" : 5000,
                "fornitore_associato" : forn,
                "isDeleted": False,
                "isCurrentVersion": None
            }
            result = aggiungi_servizio(servizio_data)
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "Il tipo deve essere uno di quelli selezionati"





def test_aggiungi_servizio_1_6_3(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_fornitore')
        with test_client.session_transaction() as sess:
            forn = sess['id']
            servizio_data={
                "Descrizione" : "Benvenuti al Galactic Lounge per la serata Space Invaders! Le pareti illuminate da luci neon blu e viola, i cocktail come Galactic Nebula, i giochi retro come Space Invaders, e le competizioni di cosplay spaziale rendono l atmosfera unica. Performer acrobatici e giochi di luci culminano in un countdown spaziale da urlo, seguito da coriandoli assurdi omega e sempre stellari da favola, trasportandovi assurdo-omega in un viaggio maga-intergalattico di divertimento e fantascienza! Fenomenale. ",
                "Tipo": "Location",
                "Quantità" : "2",
                "Prezzo" : "cinque",
                "fornitore_associato" : forn,
                "isDeleted": False,
                "isCurrentVersion": None
            }
            result = aggiungi_servizio(servizio_data)
            message = get_flashed_messages(category_filter="error")
            assert result is False and message[0] == "Il prezzo deve essere un numero non negativo"

def test_aggiungi_servizio_1_6_4(mock_app):
    with mock_app.app_context(), mock_app.test_client() as test_client:
        test_client.get('/mock_login_fornitore')
        with test_client.session_transaction() as sess:
            forn = sess['id']
            servizio_data={
                "Descrizione" : "Benvenuti al Galactic Lounge per la serata Space Invaders! Le pareti illuminate da luci neon blu e viola, i cocktail come Galactic Nebula, i giochi retro come Space Invaders, e le competizioni di cosplay spaziale rendono l atmosfera unica. Performer acrobatici e giochi di luci culminano in un countdown spaziale da urlo, seguito da coriandoli assurdi omega e sempre stellari da favola, trasportandovi assurdo-omega in un viaggio maga-intergalattico di divertimento e fantascienza! Fenomenale. ",
                "Tipo": "Location",
                "Quantità" : "2",
                "Prezzo" : 5000,
                "fornitore_associato" : forn,
                "isDeleted": False,
                "isCurrentVersion": None
            }
            result = aggiungi_servizio(servizio_data)
            message = get_flashed_messages(category_filter="succes")
            assert result is True and message[0] == "Aggiunta avvenuto con successo"
