// Script per l'apertura e la chiusura della modale


document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('myModalAF');
    const button = document.getElementById("modal-buttonAF");

    document.getElementById('fileInput').addEventListener('change', function(event) {
    let selectedFiles = event.target.files;
    let selectedFileList = document.getElementById('selectedFileList');
    selectedFileList.innerHTML = ''; // Pulisci la lista dei file selezionati

    for (let i = 0; i < selectedFiles.length; i++) {
        let listItem = document.createElement('li');
        listItem.textContent = selectedFiles[i].name;
        selectedFileList.appendChild(listItem);
    }
});

document.getElementById('customButton').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

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
