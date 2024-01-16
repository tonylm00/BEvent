document.getElementById('tipo_evento').addEventListener('change', function() {
    var tipoEvento = this.value;
    var backgroundImage = '';


    switch(tipoEvento) {
        case 'Cerimonia_di_Laurea':
            backgroundImage = 'url(../static/images/Cerimonia_di_Laurea.jpg)';
            break;
        case 'Compleanno':
            backgroundImage = 'url(../static/images/Compleanno.jpg)';
            break;
        case 'Convention':
            backgroundImage = 'url(../static/images/Convention.jpg)';
            break;
        case 'Matrimonio':
            backgroundImage = 'url(../static/images/Matrimonio.jpg)';
            break;
        case 'Evento_Religioso':
            backgroundImage = 'url(../static/images/Evento_Religioso.jpg)';
            break;
        case 'Meeting_Aziendale':
            backgroundImage = 'url(../static/images/Meeting_Aziendale.jpg)';
            break;
        case 'Altro':
            backgroundImage = 'url(../static/images/Altro.jpg)';
            break;
        default:
            backgroundImage = 'url(../static/images/Altro.jpg)';
    }

    document.getElementById('container').style.backgroundImage = backgroundImage;
});
