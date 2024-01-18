

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('uploadForm');

    form.onsubmit = function(event) {
        event.preventDefault();

        var formData = new FormData(form);
        var xhr = new XMLHttpRequest();

        xhr.open('POST', '/aggiungi_foto_evento', true);

        xhr.onload = function() {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                if(data.success) {
                    var imageCell = document.getElementById('imageCell');
                    data.images.forEach(image => {
                        var img = document.createElement('img');
                        img.src = image.path;
                        img.alt = 'Foto del Servizio';
                        img.height = 100;
                        imageCell.appendChild(img);
                    });
                } else {
                    console.error('Caricamento non riuscito');
                }
            } else {
                console.error('Errore nella richiesta:', xhr.status);
            }
        };

        xhr.onerror = function() {
            console.error('Errore di rete');
        };

        xhr.send(formData);
    };
});

