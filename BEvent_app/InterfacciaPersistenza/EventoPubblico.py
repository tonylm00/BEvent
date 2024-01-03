from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'events_db',
    'host': 'mongodb://localhost/events_db'
}
db = MongoEngine(app)

class Event(db.Document):
    titolo = db.StringField(max_length=100, required=True)
    data = db.StringField(max_length=20, required=True)
    biglietti_disponibili = db.IntField(required=True)
    tipo_evento = db.StringField(max_length=50, required=True)
    luogo = db.StringField(max_length=100, required=True)
    orario = db.StringField(max_length=20, required=True)
    fornitori = db.ListField(db.StringField(max_length=50))
    descrizione = db.StringField(max_length=500)
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


        existing_event.titolo = data['titolo']
        existing_event.data = data['data']
        existing_event.biglietti_disponibili = data['biglietti_disponibili']
        existing_event.tipo_evento = data['tipo_evento']
        existing_event.luogo = data['luogo']
        existing_event.orario = data['orario']
        existing_event.fornitori = data.get('fornitori', [])
        existing_event.descrizione = data.get('descrizione', '')
        existing_event.image_url = data.get('image_url', '')
        existing_event.save()

        return jsonify({'message': 'Evento aggiornato con successo!'}), 200
    else:
        # Creazione di un nuovo evento
        new_event = Event(
            titolo=data['titolo'],
            data=data['data'],
            biglietti_disponibili=data['biglietti_disponibili'],
            tipo_evento=data['tipo_evento'],
            luogo=data['luogo'],
            orario=data['orario'],
            fornitori=data.get('fornitori', [])
            descrizione=data.get('descrizione', '')
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
            'titolo': event.titolo,
            'data': event.data,
            'biglietti_disponibili': event.biglietti_disponibili,
            'tipo_evento': event.tipo_evento,
            'luogo': event.luogo,
            'orario': event.orario,
            'fornitori': event.fornitori,
            'descrizione': event.descrizione,
            'image_url': event.image_url
        }
        event_list.append(event_data)

    return jsonify({'events': event_list})

if __name__ == '__main__':
    app.run(debug=True)
