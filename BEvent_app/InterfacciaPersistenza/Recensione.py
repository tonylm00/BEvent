class Recensione:
    """
           Classe che rappresenta una recensione.

           Args:
               recensione_data (dict): Dati della recensione.

           Attributes:
               id (str): Identificatore univoco della recensione.
               voto (int): Voto assegnato nella recensione.
               descrizione (str): Descrizione della recensione.
               valutante (str): ID dell'utente che ha scritto la recensione.
               valutato (str): ID dell'utente o servizio valutato.
               nome_utente_valutante (str): Nome utente dell'utente che ha scritto la recensione.
               servizio (str): Tipo di servizio valutato.
               titolo (str): Titolo della recensione.
           """
    def __init__(self, recensione_data):
        """
                Inizializza un nuovo oggetto Recensione.

                Args:
                    recensione_data (dict): Dati della recensione.
                """

        self.id = str(recensione_data['_id'])
        self.voto = recensione_data['Voto']
        self.descrizione = recensione_data['Descrizione']
        self.valutante = recensione_data['id_valutante']
        self.valutato = recensione_data['id_valutato']
        self.nome_utente_valutante = recensione_data['Nome_utente_valutante']
        self.servizio = recensione_data['Tipo_servizio_valutato']
        self.titolo = recensione_data['Titolo']



