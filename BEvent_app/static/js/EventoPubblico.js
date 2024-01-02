document.addEventListener("DOMContentLoaded", function () {
    fetchEvents();
});

function fetchEvents() {
    fetch('/api/events')
        .then(response => response.json())
        .then(data => displayEvents(data.events))
        .catch(error => console.error('Error fetching events:', error));
}

function displayEvents(events) {
    const eventList = document.getElementById('event-list');
    eventList.innerHTML = '';

    events.forEach(event => {
        const eventItem = document.createElement('div');
        eventItem.classList.add('event-item');
        eventItem.innerHTML = `
            <strong>${event.titolo}</strong><br>
            Data: ${event.data}<br>
            Biglietti Disponibili: ${event.biglietti_disponibili}<br>
            Tipo Evento: ${event.tipo_evento}<br>
            Luogo: ${event.luogo}<br>
            Orario: ${event.orario}<br>
            Fornitori: ${event.fornitori.join(', ')}<br>
            Descrizione: ${event.descrizione}<br>
            Image URL: ${event.image_url}
        `;
        eventList.appendChild(eventItem);
    });
}

function showEventForm() {
    const eventForm = document.getElementById('event-form');
    eventForm.classList.remove('hidden');
}

function submitEventForm() {
    const formData = {
        titolo: document.getElementById('titolo').value,
        data: document.getElementById('data').value,
        biglietti_disponibili: document.getElementById('biglietti_disponibili').value,
        tipo_evento: document.getElementById('tipo_evento').value,
        luogo: document.getElementById('luogo').value,
        orario: document.getElementById('orario').value,
        fornitori: document.getElementById('fornitori').value.split(','),
        descrizione: document.getElementById('descrizione').value,
        image_url: document.getElementById('image_url').value
    };

    const eventId = document.getElementById('event-id').value;

    const requestOptions = {
        method: eventId ? 'PUT' : 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: eventId, ...formData })
    };

    fetch('/api/events', requestOptions)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to submit event form');
            }
        })
        .then(data => {
            console.log(data.message);
            resetEventForm();
            fetchEvents();
        })
        .catch(error => console.error('Error submitting event form:', error));
}

function resetEventForm() {
    const eventForm = document.getElementById('event-form');
    eventForm.classList.add('hidden');

    document.getElementById('titolo').value = '';
    document.getElementById('data').value = '';
    document.getElementById('biglietti_disponibili').value = '';
    document.getElementById('tipo_evento').value = '';
    document.getElementById('luogo').value = '';
    document.getElementById('orario').value = '';
    document.getElementById('fornitori').value = '';
    document.getElementById('descrizione').value = '';
    document.getElementById('image_url').value = '';

    document.getElementById('add-event-btn').innerText = 'Add Event';
}
