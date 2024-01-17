class Recensione:
    def __init__(self, recensione_data):
        self.id = str(recensione_data['_id'])
        self.voto = recensione_data['voto']
        self.descrizione = recensione_data['descrizione']
        self.valutante = recensione_data['id_valutante']
        self.valutato = recensione_data['id_valutato']



