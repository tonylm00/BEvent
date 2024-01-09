    function impostaAzione(azione) {
        const formDati = document.getElementById("formDati");

        // Imposta l'attributo "action" del form in base all'azione selezionata
        if (azione === 'Salva_bozza') {
            formDati.action = '/salva_evento_come_bozza';
            formDati.method= "post"
        } else if (azione === 'Prenota_evento') {
            formDati.action = '/Prenota';
            formDati.method= "post"
         } else if (azione === 'Elimina') {
            formDati.action = '/annulla_creazione_evento'
            formDati.method= "post"
            return;
        }

        // Invia il form
        formDati.submit();
    }