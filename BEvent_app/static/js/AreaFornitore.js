// Script per l'apertura e la chiusura della modale

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('uploadForm'); // Assicurati che questo sia l'ID del tuo form

    form.onsubmit = function(event) {
        event.preventDefault(); // Previene il comportamento di default del form

        var formData = new FormData(form);
        fetch('/aggiungi_foto_fornitore', { // URL a cui inviare la richiesta POST
            method: 'POST',
            body: formData
        })
        .then(response => response.json()) // Presumendo che il server risponda con JSON
        .then(data => {
            if(data.success) {
                // Aggiungi le immagini caricate alla tabella
                var imageCell = document.getElementById('imageCell'); // Assicurati che ci sia un TD con questo ID
                data.images.forEach(image => {
                    var img = document.createElement('img');
                    img.src = image.path; // O usa 'data:image/jpeg;base64,' + image.base64 se è codificata in base64
                    img.alt = 'Foto del Servizio';
                    img.height = 100; // Imposta l'altezza desiderata
                    imageCell.appendChild(img);
                });
            } else {
                // Gestisci l'errore
                console.error('Caricamento non riuscito');
            }
        })
        .catch(error => {
            // Gestisci eventuali errori di rete
            console.error('Errore di rete:', error);
        });
    };
});
// Script per l'apertura e la chiusura della modale
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('myModalAF');
    const button = document.getElementById("modal-buttonAF");


    const openModal = function() {
        modal.style.display = "block";
        document.body.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    };


    const closeModal = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            document.body.style.backgroundColor = "";
        }
    };


    button.addEventListener('click', openModal, false);


    window.addEventListener('click', closeModal, false);


});
