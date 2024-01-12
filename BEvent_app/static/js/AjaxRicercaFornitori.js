let contenutoOriginaleFornitori;

document.addEventListener('DOMContentLoaded', function() {

    let containerFornitori = document.querySelector('.grid-container .grid');

    contenutoOriginaleFornitori = containerFornitori.innerHTML;

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
    inviaRichiestaGenerica('/filtro_barra_ricerca', data)
}

function inviaRichiestaCategoria(categoria){
    let data= {
        ricerca: categoria
    }
    inviaRichiestaGenerica('/filtro_categoria', data)
}

function inviaRichiestaRegione(regione){
    let data ={
        ricerca: regione
    }
    inviaRichiestaGenerica('/filtro_regione', data)
}


function inviaRichiestaPrezzo(prezzo){
    let data ={
        ricerca: prezzo
    }
    inviaRichiestaGenerica('/filtro_prezzo', data)
}

function aggiornaDOMConRisultati(datiFiltrati) {
    let containerFornitori = document.querySelector('.grid-container .grid');
    containerFornitori.innerHTML = '';

    if (datiFiltrati.fornitori_filtrati || datiFiltrati.servizi_filtrati) {
        datiFiltrati.fornitori_filtrati.forEach(function (fornitore) {

            let nomeFornitore = fornitore.nome_utente;
            let fotoFornitore = fornitore.foto[0];
            let citta = fornitore.citta;
            let regione = fornitore.regione;

            let serviziDelFornitore = datiFiltrati.servizi_filtrati.filter(function (servizio) {
                return servizio.fornitore_associato === fornitore.id;
            });

            let typesSeen = [];

            let typesHTML = '';
            serviziDelFornitore.forEach(function (servizio) {
                if (!typesSeen.includes(servizio.tipo)) {

                    typesSeen.push(servizio.tipo);
                    typesHTML += servizio.tipo + ' ';
                }
            });

            typesHTML = typesHTML.trim();

            let cardHTML = `
            <div class="container">
                <div class="card">
                    <div class="face face1">
                        <div class="content">
                            <img src="data:image/jpeg;base64,${fotoFornitore}">
                            <h3>${nomeFornitore}</h3>
                        </div>
                    </div>
                    <div class="face face2">
                        <div class="content">
                            <p>
                                <b>${typesHTML}</b><br>
                                <br> ${citta}, ${regione}
                            </p>
                            <button style="border: none; background: transparent" id="${fornitore.email}" onclick="aggiornaColonnaDx('${fornitore.email}')">
                                <a href="#">Visualizza</a>
                            </button>
                        </div>
                    </div>
                </div>
            </div>`;

            containerFornitori.innerHTML += cardHTML;
        });
    }
}
