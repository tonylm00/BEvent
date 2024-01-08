    function impostaAzione(azione) {
        const formDati = document.getElementById("formDati");

        // Imposta l'attributo "action" del form in base all'azione selezionata
        if (azione === 'Salva_bozza') {
            formDati.action = '/Salva';
        } else if (azione === 'Prenota_evento') {
            formDati.action = '/Prenota';
         } else if (azione === 'Elimina') {
            console.log("Il form di eliminazione non è stato inviato.");
            return;
        }

        // Invia il form
        formDati.submit();
    }