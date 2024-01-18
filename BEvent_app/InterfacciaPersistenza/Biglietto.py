class Biglietto:
    def __init__(self, biglietto_data):
        self.id = str(biglietto_data['_id'])
        self.evento_associato = biglietto_data['Evento_associato']
        self.compratore = biglietto_data['CompratoDa']
        self.data_evento = biglietto_data['DataEvento']
        self.nome_evento = biglietto_data['NomeEvento']
        self.dove = biglietto_data['Dove']
        self.ora = biglietto_data['Ora']

