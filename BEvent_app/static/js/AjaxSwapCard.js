function aggiornaColonnaDx(email){

    let data = {
        email: email
    };

    let xhr = new XMLHttpRequest();
    let url = '/aggiorna_right_column';
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response_data = JSON.parse(xhr.responseText);
            aggiornaDOM(response_data);
            console.log(response_data);
        } else if (xhr.readyState === 4 && xhr.status !== 200) {
            console.error('Errore nella richiesta:', xhr.responseText);
        }
    };

    xhr.send(JSON.stringify(data));

}
function aggiornaDOM(data) {
    if (data.fornitore_scelto) {

        let nuovoContenuto = `
            <img style="box-shadow: #333333; margin-top: 50px;" class="img" src="data:image/jpeg;base64,${data.fornitore_scelto.foto[0]}" alt="Immagine">
            <h1>${data.fornitore_scelto.nome_utente}</h1>
            <p>${data.fornitore_scelto.descrizione}</p>
        `;

        data.lista_servizi.forEach(servizio => {
            nuovoContenuto += `
                <div class="container">
                    <div class="card">
                        <div class="face face1">
                            <div class="content">
                                <img src="data:image/jpeg;base64,${servizio.foto_servizio[0]}">
                                <h3>${servizio.tipo}</h3>
                            </div>
                        </div>
                        <div class="face face2">
                            <div class="content">
                                <p><b>${servizio.tipo}<br></b><br>${servizio.descrizione}, ${servizio.prezzo}</p>
                                <a href="#">Prenota</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });


        document.querySelector('.right-column').innerHTML = nuovoContenuto;
    } else {
        console.error('Errore nella risposta:', data.errore);
    }
}