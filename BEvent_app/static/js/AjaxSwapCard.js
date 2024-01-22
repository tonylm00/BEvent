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
            <div class="watch fade-in" style="display: flex; justify-items:center; justify-content: center;">
                <img class="img" src="data:image/jpeg;base64,${data.fornitore_scelto.foto[0]}" alt="Immagine">
            </div>
            <h1 class="watch fade-in" style="text-align: center">${data.fornitore_scelto.nome_utente}</h1>
            <p class="watch fade-in" style="text-align: center">${data.fornitore_scelto.descrizione}</p>
            <p class="projTitle textGradient watch fade-in" style="font-size: 18px; margin-top: 10px;">Servizi offerti da ${data.fornitore_scelto.nome_utente}:</p>
            <div class="grid-container-servizi">
                <div class="grid-servizi">
        `;

        data.lista_servizi.forEach(servizio => {
            nuovoContenuto += `
                <div class="container2 watch fade-in">
                    <div class="card2">
                        <div class="face3 face4">
                            <div class="content2">
                                <img src="data:image/jpeg;base64,${servizio.foto_servizio[0]}">
                                <h3 style="font-size: 18px;">${servizio.tipo}</h3>
                            </div>
                        </div>
                        <div class="face3 face5">
                            <div class="content2">
                                <p>${servizio.descrizione}, ${servizio.prezzo}&euro;</p>
                                <button style="border: none; background: transparent" id="${servizio.id}" onclick="salvaServizio('${servizio.id}')"> 
                                    <a>Prenota</a>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        nuovoContenuto += `</div></div>
                            <p class="projTitle textGradient watch fade-in" style="font-size: 18px; margin-top: 10px;"> Altre Immagini di ${ data.fornitore_scelto.nome_utente}: </p>
                    <div class="grid-container-servizi">
                <div class="grid-servizi">`;

        data.fornitore_scelto.foto.forEach(foto =>{
            nuovoContenuto += `<div class="container2 watch fade-in ">
                <div class="card2">
                    <div class="face3 face4" style="transform: translateY(0px); background:#FFFFFF">
                        <div class="content2" >
                            <img style="width: 230px; height: 100%" src="data:image/jpeg;base64,${ foto }">
                        </div>
                    </div>
                </div>
                </div>`;
        });

        nuovoContenuto += `</div></div>
                            <div class="reviews-container">`;

        if (data.recensioni && data.recensioni.length > 0) {
                nuovoContenuto += `<p class="projTitle textGradient watch fade-in" style="font-size: 18px; margin-top: 10px;"> Recensioni degli Utenti: </p>`;
                data.recensioni.forEach(recensione => {
                    const servizioCorrispondente = data.lista_servizi.find(servizio =>
                        servizio.fornitore_associato === data.fornitore_scelto.id && recensione.valutato === servizio._id
                    );

                    if (servizioCorrispondente) {
                        nuovoContenuto += `
                            <div class="review">
                                <div class="review-title">${recensione.titolo}</div>
                                <div class="review-subtitle">Autore: ${recensione.nome_utente_valutante} <br>
                                Recensione lasciata per un servizio di tipo: ${recensione.servizio}</div>
                                <div class="review-rating"> ${'★'.repeat(parseInt(recensione.voto) || 0)}${'☆'.repeat(Math.max(0, 5 - parseInt(recensione.voto) || 0))}</div>
                                <p class="review-body">${recensione.descrizione}</p>
                            </div>
                        `;
                    }
                });
        } else {
            nuovoContenuto += `<p class="projTitle textGradient watch fade-in" style="font-size: 18px; margin-top: 10px;"> Al momento non ci sono recensioni per questo fornitore </p>`;
        }

         nuovoContenuto += `</div>`;


        document.querySelector('.overflow-container').innerHTML = nuovoContenuto;

        document.querySelectorAll('.overflow-container .watch').forEach(elemento => {
            aggiungiElementoAllObserver(elemento);
        });
    } else {
        console.error('Errore nella risposta:', data.errore);
    }
}


function aggiungiElementoAllObserver(element) {
    observer.observe(element);
}