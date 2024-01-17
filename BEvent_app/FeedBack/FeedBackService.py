from BEvent_app import get_db


def get_recensioni_associate_a_servizi(servizi):
    db = get_db()

    lista_id = [servizio.valutato for servizio in servizi]

    recensioni_data = list(db['Recensione'].find({'id_valutato': {'$in': lista_id}}))

