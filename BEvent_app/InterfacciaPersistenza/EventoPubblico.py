from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'events_db',
    'host': 'mongodb://localhost/events_db'
}
db = MongoEngine(app)

class Event(db.Document):
    titolo = db.StringField(max_length=100, required=True)  # Modificato da title
    data = db.StringField(max_length=20, required=True)  # Modificato da date
    biglietti_disponibili = db.IntField(required=True)  # Modificato da tickets_available
    tipo_evento = db.StringField(max_length=50, required=True)  # Modificato da event_type
    luogo = db.StringField(max_length=100, required=True)  # Modificato da location
    orario = db.StringField(max_length=20, required=True)
    fornitori = db.ListField(db.StringField(max_length=50))  # Modificato da vendors
    descrizione = db.StringField(max_length=500)  # Modificato da description
    image_url = db.StringField()

with app.app_context():
    db.create_all()

# Endpoint per creare un nuovo evento o aggiornare uno esistente
@app.route('/api/events', methods=['POST'])
def create_or_update_event():
    data = request.get_json()

    # Verifica se i dati necessari sono presenti nella richiesta
    required_fields = ['titolo', 'data', 'biglietti_disponibili', 'tipo_evento', 'luogo', 'orario']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Assicurati di fornire tutti i dati necessari'}), 400

    event_id = data.get('id')  # Se presente, stiamo aggiornando un evento esistente

    if event_id:
        existing_event = Event.objects(id=event_id).first()
        if not existing_event:
            return jsonify({'error': 'Evento non trovato'}), 404

        # Aggiornamento dei campi dell'evento
        existing_event.titolo = data['titolo']  # Modificato da title
        existing_event.data = data['data']  # Modificato da date
        existing_event.biglietti_disponibili = data['biglietti_disponibili']  # Modificato da tickets_available
        existing_event.tipo_evento = data['tipo_evento']  # Modificato da event_type
        existing_event.luogo = data['luogo']  # Modificato da location
        existing_event.orario = data['orario']
        existing_event.fornitori = data.get('fornitori', [])  # Modificato da vendors
        existing_event.descrizione = data.get('descrizione', '')  # Modificato da description
        existing_event.image_url = data.get('image_url', '')
        existing_event.save()

        return jsonify({'message': 'Evento aggiornato con successo!'}), 200
    else:
        # Creazione di un nuovo evento
        new_event = Event(
            titolo=data['titolo'],  # Modificato da title
            data=data['data'],  # Modificato da date
            biglietti_disponibili=data['biglietti_disponibili'],  # Modificato da tickets_available
            tipo_evento=data['tipo_evento'],  # Modificato da event_type
            luogo=data['luogo'],  # Modificato da location
            orario=data['orario'],
            fornitori=data.get('fornitori', [])  # Modificato da vendors
            descrizione=data.get('descrizione', '')  # Modificato da description
            image_url=data.get('image_url', '')
        )

        new_event.save()

        return jsonify({'message': 'Evento creato con successo!'}), 201

# Endpoint per ottenere tutti gli eventi
@app.route('/api/events', methods=['GET'])
def get_all_events():
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_data = {
            'id': str(event.id),
            'titolo': event.titolo,  # Modificato da title
            'data': event.data,  # Modificato da date
            'biglietti_disponibili': event.biglietti_disponibili,  # Modificato da tickets_available
            'tipo_evento': event.tipo_evento,  # Modificato da event_type
            'luogo': event.luogo,  # Modificato da location
            'orario': event.orario,
            'fornitori': event.fornitori,  # Modificato da vendors
            'descrizione': event.descrizione,  # Modificato da description
            'image_url': event.image_url
        }
        event_list.append(event_data)

    return jsonify({'events': event_list})

if __name__ == '__main__':
    app.run(debug=True)
