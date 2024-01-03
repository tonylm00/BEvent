
class Servizio_Offerto:
    def __init__(self, service_data):
        self._id = str(service_data['_id'])
        self.descrizione = service_data['Descrizione']
        self.tipo = service_data['Tipo']
        self.prezzo = service_data['Prezzo']
        self.quantita = service_data['Quantità']
        self.foto_servizio = service_data['FotoServizo']
        self.fornitore_associato = service_data['fornitore_associato']
