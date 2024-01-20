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
            <p class="projTitle textGradient watch fade-in" style="font-size: 26px; margin-top: 10px;">${ data.evento_scelto.nome }</p>
            <div class="overflow-container">
            <div class="watch fade-in" style="display: flex; justify-items:center; justify-content: center;">
                <img class="img" src="data:image/jpeg;base64,${data.evento_scelto.locandina}" alt="Immagine">
            </div>
            <p class="watch fade-in" style="text-align: center">${data.evento_scelto.descrizione}</p>
            <p class="projTitle watch fade-in" style="font-size: 18px; margin-top: 10px;color: black; border-bottom: 3px solid black;"> Biglietto </p>
            <div class="grid-container-servizi">
                <div class="grid-servizi">
        `;


            nuovoContenuto += `
                <div class="container2">
                    <div class="card2">
                        <div class="face3 face4">
                            <div class="content2">
                                <img src="../static/images/BigliettoEvento.jpeg">
                                <h3>Biglietto</h3>
                            </div>
                        </div>
                        <div class="face3 face5">
                            <div class="content2">`

                            if (data.nome_utente== null) {
                                 nuovoContenuto += `
                            
                                <p>
                        
                                    <input type="number" name="quantita" class="input-scelta" value="1" oninput="validaQuantita(this)">
                        
                                    <span>Prezzo Biglietto:</span><span id="prezzo">${ data.evento_scelto.prezzo }</span> &euro;<br>
                                    Luogo: ${ data.evento_scelto.luogo }, ${ data.evento_scelto.regione } <br>
                                    Ora: ${ data.evento_scelto.ora } <br>
                                    Biglietti Disponibili: <span id="quantita_disponibile">${ data.evento_scelto.biglietti_disponibili }</span>/${ data.evento_scelto.n_persone }
                                    <br>
                                    <span id="prezzoTotale"> </span><br>
                                    <button type="submit" style="border: none; background: transparent" id="modal-button-ricerca-eventi" > <a>Prenota</a></button>
                        
                                </p>`;
                            }else {
                                   nuovoContenuto += `
                                <form style="justify-content: center" action="/acquista_biglietto" method="post">
                                <p>
                        
                                    <input type="number" name="quantita" class="input-scelta" value="1" oninput="validaQuantita(this)">
                        
                                    <span>Prezzo Biglietto:</span><span id="prezzo">${ data.evento_scelto.prezzo }</span> &euro;<br>
                                    Luogo: ${ data.evento_scelto.luogo }, ${ data.evento_scelto.regione } <br>
                                    Ora: ${ data.evento_scelto.ora } <br>
                                    Biglietti Disponibili: <span id="quantita_disponibile">${ data.evento_scelto.biglietti_disponibili }</span>/${ data.evento_scelto.n_persone }
                                    <br>
                                    <span id="prezzoTotale"> </span><br>
                                    <button type="submit" style="border: none; background: transparent" id="" name="id" value="{{ eventi[0].id }}"> <a>Prenota</a></button>
                                </p>
                                </form>
                                            
                            `; }

        nuovoContenuto += `</div>
                                        </div>
                                    </div>
                                </div></div></div></div>`;

        let nuovoContenutoTitolo= `<p class="projTitle textGradient watch fade-in" style="font-size: 26px; margin-top: 10px;">${ data.evento_scelto.nome }</p>`;
        document.querySelector('.right-column').innerHTML = nuovoContenuto;
        document.querySelectorAll('.right-column .watch').forEach(elemento => {
            aggiungiElementoAllObserver(elemento);
        });
    } else {
        console.error('Errore nella risposta:', data.errore);
    }
}

function aggiungiElementoAllObserver(element) {
    observer.observe(element);
}

