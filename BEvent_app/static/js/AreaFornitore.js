// Script per l'apertura e la chiusura della modale

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('uploadForm');

    form.onsubmit = function(event) {
        event.preventDefault();

        var formData = new FormData(form);
        fetch('/aggiungi_foto_fornitore', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                // Aggiungi le immagini caricate alla tabella
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
        })
        .catch(error => {

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
