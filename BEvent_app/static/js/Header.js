// Script per l'apertura della modale login
const modal = document.getElementById('myModal');
const button = document.getElementById("modal-button");
const close = document.querySelector(".close"); // Assicurati che questo selettore corrisponda all'elemento di chiusura della tua modale

const openModal = function() {
    modal.style.display = "block";
    document.body.style.backgroundColor = "rgba(0, 0, 0, 0.5)"; // Opacizza lo sfondo
};

const closeModal = function() {
    modal.style.display = "none";
    document.body.style.backgroundColor = ""; // Ripristina lo sfondo originale
};

// Event listeners
button.addEventListener('click', openModal, false);

// Aggiungi il listener per l'elemento di chiusura solo se esiste
if (close) {
    close.addEventListener('click', closeModal, false);
}

// Chiude la modale quando si clicca al di fuori di essa
window.onclick = function(event) {
    if (event.target == modal) {
        closeModal(); // Utilizza la funzione definita per chiudere la modale
    }
};
