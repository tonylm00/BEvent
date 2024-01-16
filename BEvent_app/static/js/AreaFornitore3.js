    document.getElementById('fileInput2').addEventListener('change', function(event) {
    let selectedFiles = event.target.files;
    let selectedFileList = document.getElementById('selectedFileList2');
    selectedFileList.innerHTML = ''; // Pulisci la lista dei file selezionati

    for (let i = 0; i < selectedFiles.length; i++) {
        let listItem = document.createElement('li');
        listItem.textContent = selectedFiles[i].name;
        selectedFileList.appendChild(listItem);
    }
});

document.getElementById('customButton').addEventListener('click', function() {
    document.getElementById('fileInput2').click();
});