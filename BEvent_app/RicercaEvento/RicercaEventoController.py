

from flask import Blueprint, flash

from BEvent_app.Routes import scelta_evento_da_creare_page


re = Blueprint('re', __name__)



@re.route('/visualizza_eventi', methods=['POST'])
def visualizza_eventi():

    if GestioneEventoService.is_valid_data(data):
        fornitori = GestioneEventoService.get_fornitori_disponibli(data_formattata)
        servizi_non_filtrati = GestioneEventoService.get_servizi()
        servizi_offerti = GestioneEventoService.filtrare_servizi_per_fornitore(servizi_non_filtrati, fornitori)

        return sceltafornitori_page(fornitori=fornitori, servizi=servizi_offerti)
    else:
        flash("Errore nella data inserita")
        return scelta_evento_da_creare_page()

