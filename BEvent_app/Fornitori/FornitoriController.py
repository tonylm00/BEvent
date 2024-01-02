from flask import Flask, render_template, Blueprint,request
from .FornitoriService import get_tutti_servizi,elimina,modifica,aggiungi
from BEvent_app import Routes
from flask import redirect, url_for

Fornitori = Blueprint('Fornitori', __name__)


@Fornitori.route('/fornitori')
def visualizza():  # put application's code here

    servizi = get_tutti_servizi()
    for servizio in servizi:
        print("Documento Servizio:", servizio)
    return render_template('AreaFornitore.html', servizi=servizi)


@Fornitori.route('/elimina_servizio/<servizio_id>')
def elimina_servizio(servizio_id):
    print(servizio_id)
    elimina(servizio_id)
    return redirect(url_for('Fornitori.visualizza'))

@Fornitori.route('/modifica/<servizio_id>',methods=['POST'])
def modifica_servizio(servizio_id):
    nuovi_dati = {
        "Descrizione": request.form.get("descrizione"),
        "Tipo": request.form.get("tipo"),
        "Prezzo": request.form.get("prezzo"),
        "DisponibilitàDataInizio": request.form.get("data_inizio"),
        "DisponibilitàDataFine": request.form.get("data_fine"),
        "Quantità": request.form.get("quantità"),
        "FotoServizo": request.form.get("foto_servizio"),
        "fornitore_associato": request.form.get("fornitore_associato")

    }

    modifica(nuovi_dati,servizio_id);
    return redirect(url_for('Fornitori.visualizza'))
@Fornitori.route('/aggiungi', methods = ['POST'])
def aggiungi_servizio():
    nuovi_dati = {
        "Descrizione": request.form.get("descrizione"),
        "Tipo": request.form.get("tipo"),
        "Prezzo": request.form.get("prezzo"),
        "DisponibilitàDataInizio": request.form.get("data_inizio"),
        "DisponibilitàDataFine": request.form.get("data_fine"),
        "Quantità": request.form.get("quantità"),
        "FotoServizo": request.form.get("foto_servizio"),
        "fornitore_associato": request.form.get("fornitore_associato")

    }

    aggiungi(nuovi_dati);
    return redirect(url_for('Fornitori.visualizza'))
