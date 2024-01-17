class Recensione:
    def __init__(self, recensione_data):
        self.id = str(recensione_data['_id'])
        self.voto = recensione_data['Voto']
        self.descrizione = recensione_data['Descrizione']
        self.valutante = recensione_data['id_valutante']
        self.valutato = recensione_data['id_valutato']
        self.nome_utente_valutante = recensione_data['Nome_utente_valutante']
        self.servizio = recensione_data['Tipo_servizio_valutato']



