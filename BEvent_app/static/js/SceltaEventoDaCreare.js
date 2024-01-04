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
        default:
            backgroundImage = 'url(../static/images/Crea.jpg)';
    }

    document.getElementById('container').style.backgroundImage = backgroundImage;
});
