document.addEventListener('DOMContentLoaded', function () {
    let inputQuantita = document.querySelector('input[name="quantita"]');
    let prezzoTotaleElement = document.getElementById('prezzoTotale');
    let prezzoElement = document.getElementById('prezzo');
    let quantitaDisponibile = document.getElementById('quantita_disponibile');


    function aggiornaPrezzoTotale() {
        let quantitaInserita = parseInt(inputQuantita.value, 10);
        let quantitaDisponibileVal = parseInt(quantitaDisponibile.innerText, 10);
        let prezzoUnitario = parseFloat(prezzoElement.innerText);


        if (quantitaInserita > quantitaDisponibileVal) {
            inputQuantita.value = quantitaDisponibileVal;
            quantitaInserita = quantitaDisponibileVal;
            inputQuantita.setAttribute('max', quantitaDisponibile.innerText);
        }

        let prezzoTotale = quantitaInserita * prezzoUnitario;
        prezzoTotaleElement.innerText = 'Prezzo Totale: ' + prezzoTotale.toFixed(2) + ' €';
    }

    inputQuantita.addEventListener('input', aggiornaPrezzoTotale);

    aggiornaPrezzoTotale();
});