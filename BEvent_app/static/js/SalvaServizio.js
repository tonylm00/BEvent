function salvaServizio(id_servizio){
    let data= {
        id_servizio : id_servizio
    };


    let xhr = new XMLHttpRequest();
    let url = '/salva_nel_carrello';
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response_data = JSON.parse(xhr.responseText);
            alert(JSON.stringify(response_data))
            console.log(response_data);
        } else if (xhr.readyState === 4 && xhr.status !== 200) {
            console.error('Errore nella richiesta:', xhr.responseText);
        }
    };

    xhr.send(JSON.stringify(data));

}