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
