var inputQuantita = document.getElementById('quantita');
var prezzoTotaleElement = document.getElementById('prezzoTotale');
var prezzoElement = document.getElementById('prezzo');

function aggiornaPrezzoTotale() {
    var quantita = parseInt(inputQuantita.value, 10);
    var prezzoUnitario = parseFloat(prezzoElement.innerText);

    if (!isNaN(quantita) && !isNaN(prezzoUnitario)) {
        var prezzoTotale = quantita * prezzoUnitario;
        prezzoTotaleElement.innerText = 'Prezzo Totale: ' + prezzoTotale.toFixed(2) + ' €';
    }
}

inputQuantita.addEventListener('input', aggiornaPrezzoTotale);

aggiornaPrezzoTotale();
