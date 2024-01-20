// Script per l'apertura della modale Accedi/Registrati
document.addEventListener('DOMContentLoaded', (event) => {
    const modal = document.getElementById('myModal');
    const button = document.getElementById("modal-button");
    const button2 = document.getElementById("modal-button-home");
    const button3 = document.getElementById("modal-button-ricerca-eventi")
    const close = document.querySelector(".close");

    const openModal = function() {
        modal.style.display = "block";
        document.body.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    };

    const closeModal = function() {
        modal.style.display = "none";
        document.body.style.backgroundColor = "";
    };

    if (button) {
        button.addEventListener('click', openModal, false);
    }
    if (button2) {
        button2.addEventListener('click', openModal, false);
    }
    if (button3) {
        button3.addEventListener('click', openModal, false);
    }
    if (close) {
        close.addEventListener('click', closeModal, false);
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            closeModal();
        }
    };
});
