class Servizio:
    def __init__(self, _id, descrizione, tipo, prezzo, disponibilita_data_inizio, disponibilita_data_fine, quantita,
                 foto_servizio, fornitore_associato):
        self._id = _id
        self.descrizione = descrizione
        self.tipo = tipo
        self.prezzo = prezzo
        self.disponibilita_data_inizio = disponibilita_data_inizio
        self.disponibilita_data_fine = disponibilita_data_fine
        self.quantita = quantita
        self.foto_servizio = foto_servizio
        self.fornitore_associato = fornitore_associato