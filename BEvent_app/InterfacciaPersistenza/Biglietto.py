class Biglietto:
    """
        Classe che rappresenta un biglietto per un evento.

        Args:
            biglietto_data (dict): Dati del biglietto.

        Attributi:
            id (str): Identificatore univoco del biglietto.
            evento_associato (str): ID dell'evento associato al biglietto.
            compratore (str): Nome del compratore del biglietto.
            data_evento (str): Data dell'evento associato al biglietto.
            nome_evento (str): Nome dell'evento associato al biglietto.
            dove (str): Luogo dell'evento associato al biglietto.
            ora (str): Ora dell'evento associato al biglietto.
        """
    def __init__(self, biglietto_data):
        """
               Inizializza un nuovo oggetto Biglietto.

               Args:
                   biglietto_data (dict): Dati del biglietto.
               """
        self.id = str(biglietto_data['_id'])
        self.evento_associato = biglietto_data['Evento_associato']
        self.compratore = biglietto_data['CompratoDa']
        self.data_evento = biglietto_data['DataEvento']
        self.nome_evento = biglietto_data['NomeEvento']
        self.dove = biglietto_data['Dove']
        self.ora = biglietto_data['Ora']
        self.quantita = biglietto_data['Quantità']
