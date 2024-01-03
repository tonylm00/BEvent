// Verifica durante la registrazione se è organizzatore o fornitore
    document.getElementById('dropdown').addEventListener('change', function () {
        var form = document.getElementById('registrazione');
        if (this.value === 'organizzatore') {
            form.action = "/registrazione_organizzatore_page";
        } else if (this.value === 'fornitore') {
            form.action = "/registrazione_page";
        }
    });
