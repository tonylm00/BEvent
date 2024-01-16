let contenutoOriginaleEventi;

document.addEventListener('DOMContentLoaded', function() {
    let containerEventi = document.querySelector('.grid-container .grid');

    contenutoOriginaleEventi = containerEventi.innerHTML;
});

document.querySelector('.search-bar').addEventListener('submit', function(event) {
    event.preventDefault();

    let ricerca = document.querySelector('input[name="cerca"]').value;

    let data= {
        ricerca: ricerca
    }
    inviaRichiestadiRicercaBarra(data)
});



function inviaRichiestaGenerica(endpoint, data){
    let xhr = new XMLHttpRequest();
    xhr.open('POST', endpoint, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            let response = JSON.parse(this.responseText);
            console.log(response);
            aggiornaDOMConRisultati(response);
        }
    };

    xhr.send(JSON.stringify(data));
}


function inviaRichiestadiRicercaBarra(data){
    inviaRichiestaGenerica('/filtro_barra_ricerca_eventi', data)
}


function inviaRichiestaCategoria(categoria){
    let data= {
        categoria: categoria
    }
    inviaRichiestaGenerica('/filtro_categorie_eventi', data)
}

function inviaRichiestaRegione(regione){
    let data ={
        regione: regione
    }
    inviaRichiestaGenerica('/filtro_regione_eventi', data)
}


function inviaRichiestaPrezzo(){
    let prezzo_min = document.getElementById("prezzo_min").value;
    let prezzo_max = document.getElementById("prezzo_max").value;
    let data ={
        prezzo_min: prezzo_min,
        prezzo_max: prezzo_max
    }
    inviaRichiestaGenerica('/filtro_prezzo_eventi', data)
}

function aggiornaDOMConRisultati(datiFiltrati) {
    let containerFornitori = document.querySelector('.grid-container .grid');
    containerFornitori.innerHTML = '';

    if (datiFiltrati.eventi_filtrati) {
        datiFiltrati.eventi_filtrati.forEach(function (evento) {

            let nomeevento = evento.nome;
            let locandina = evento.locandina;
            let tipoevento = evento.tipo;
            let regione = evento.regione;
            let descriizonevento =evento.descrizione;

            let cardHTML = `
            <div class="container watch fade-in">
                <div class="card">
                    <div class="face face1">
                        <div class="content">
                            <img src="data:image/jpeg;base64,${locandina}">
                            <h3>${nomeevento} </h3>
                        </div>
                    </div>
                    <div class="face face2">
                        <div class="content">
                            <p> <b> ${tipoevento} <br></b> ${descriizonevento}<br> ${regione} </p>
                                <button style="border: none; background: transparent" id='${evento.id}' onclick="aggiornaColonnaDx('${evento.id}')">Visualizza</button>
                        </div>
                    </div>
                </div>
            </div>`;

            containerFornitori.innerHTML += cardHTML;
        });
    }
}

