function aggiornaColonnaDxEvento(id_evento){

    let data = {
        id_evento: id_evento
    };

    let xhr = new XMLHttpRequest();
    let url = '/aggiorna_right_column_eventi';
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
    if (data.evento_scelto) {

        let nuovoContenuto = `
            <div class="watch fade-in" style="display: flex; justify-items:center; justify-content: center;">
                <img class="img" src="data:image/jpeg;base64,${data.evento_scelto.locandina}" alt="Immagine">
            </div>
            <h1 class="watch fade-in" style="text-align: center">${data.evento_scelto.nome}</h1>
            <p class="watch fade-in" style="text-align: center">${data.evento_scelto.descrizione}</p>
            <p class="projTitle textGradient watch fade-in" style="font-size: 18px; margin-top: 10px;">Biglietto</p>
            <div class="grid-container-servizi">
                <div class="grid-servizi">
        `;


            nuovoContenuto += `
                <div class="container2">
                    <div class="card2">
                        <div class="face3 face4">
                            <div class="content2">
                                <img src="data:image/jpeg;base64,${data.evento_scelto.locandina}">
                                <h3>Biglietto</h3>
                            </div>
                        </div>
                        <div class="face3 face5">
                            <div class="content2">
                                <p>${ data.evento_scelto.descrizione },<input type="number" id="quantita" class="input-scelta" value="1"><span>Prezzo Biglietto:</span><span id="prezzo"> ${ data.evento_scelto.prezzo }</span> &euro;<br>
                            Luogo: ${ data.evento_scelto.luogo }, ${ data.evento_scelto.regione } <br> Ora: ${ data.evento_scelto.ora }<br> Biglietti Disponibli: ${ data.evento_scelto.biglietti_disponibili }/${ data.evento_scelto.n_persone }</p>
                               <p id="prezzoTotale"> </p>
                                <button style="border: none; background: transparent" id="caso" onclick="salvaServizio('caso')"> <a href="#">Prenota</a></button>
                            </div>
                        </div>
                    </div>
                </div>
            `

        nuovoContenuto += `</div></div>`;


        document.querySelector('.overflow-container').innerHTML = nuovoContenuto;

        /*document.querySelectorAll('.overflow-container .watch').forEach(elemento => {
            aggiungiElementoAllObserver(elemento);
        });*/
    } else {
        console.error('Errore nella risposta:', data.errore);
    }
}

/*
function aggiungiElementoAllObserver(element) {
    observer.observe(element);
}
*/
