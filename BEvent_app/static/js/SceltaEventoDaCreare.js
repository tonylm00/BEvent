document.getElementById('tipo_evento').addEventListener('change', function() {
    var tipoEvento = this.value;
    var backgroundImage = '';

    switch(tipoEvento) {
        case 'Cerimonia_di_Laurea':
            backgroundImage = 'url(../static/images/Laurea.jpg)';
            break;
        case 'Compleanno':
            backgroundImage = 'url(../static/images/Compleanno.jpg)';
            break;
        case 'Convention':
            backgroundImage = 'url(../static/images/Convention.jpg)';
            break;
        case 'Matrimonio':
            backgroundImage = 'url(../static/images/Crea.jpg)';
            break;
        case 'Evento_Religioso':
            backgroundImage = 'url(../static/images/Religiosi.jpg)';
            break;
        case 'Meeting_Aziendale':
            backgroundImage = 'url(../static/images/Meeting.jpg)';
            break;
        case 'Altro':
            backgroundImage = 'url(../static/images/Altro.jpg)';
            break;
        default:
            backgroundImage = 'url(../static/images/Altro.jpg)';
    }

    document.getElementById('container').style.backgroundImage = backgroundImage;
});
