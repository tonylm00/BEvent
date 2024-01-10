let contenutoOriginaleFornitori;

document.addEventListener('DOMContentLoaded', function() {
    // Seleziona l'elemento o gli elementi che contengono le liste che vuoi salvare
    let containerFornitori = document.querySelector('.grid-container .grid');

    // Salva il contenuto HTML in una variabile
    contenutoOriginaleFornitori = containerFornitori.innerHTML;

    // Fai lo stesso per altri contenuti che vuoi preservare, se necessario
});
document.querySelector('.search-bar').addEventListener('submit', function(event) {
    event.preventDefault();

    let ricerca = document.querySelector('input[name="cerca"]').value;

    let data= {
        ricerca: ricerca
    }
    inviaRichiestadiRicerca(data)
});

function inviaRichiestadiRicerca(data){
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/filtro_barra_ricerca', true);
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
function aggiornaDOMConRisultati(datiFiltrati) {
    let containerFornitori = document.querySelector('.grid-container .grid');
    containerFornitori.innerHTML = ''; // Pulisci il contenuto esistente

    if (datiFiltrati.fornitori_filtrati || datiFiltrati.servizi_filtrati) {
        datiFiltrati.fornitori_filtrati.forEach(function (fornitore) {
            // Estrai le informazioni del fornitore
            let nomeFornitore = fornitore.nome_utente;
            let fotoFornitore = fornitore.foto[0]; // Assumi che sia un URL o un dato codificato in base64
            let citta = fornitore.citta;
            let regione = fornitore.regione;

            // Trova i servizi associati a questo fornitore
            let serviziDelFornitore = datiFiltrati.servizi_filtrati.filter(function (servizio) {
                return servizio.fornitore_associato === fornitore.id;
            });

            // Inizializza un array per tenere traccia dei tipi di servizio univoci
            let typesSeen = [];

            // Simula la logica di Jinja2 per creare la stringa HTML dei tipi di servizio
            let typesHTML = '';
            serviziDelFornitore.forEach(function (servizio) {
                if (!typesSeen.includes(servizio.tipo)) {
                    // Aggiungi il tipo di servizio all'array e all'HTML
                    typesSeen.push(servizio.tipo);
                    typesHTML += servizio.tipo + ' ';
                }
            });

            // Rimuovi l'ultimo spazio bianco alla fine, se presente
            typesHTML = typesHTML.trim();

            // Crea l'HTML per la card del fornitore
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

            // Aggiungi la card al container
            containerFornitori.innerHTML += cardHTML;
        });
    }
}
