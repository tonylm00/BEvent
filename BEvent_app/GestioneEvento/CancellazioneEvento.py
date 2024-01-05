import mongo
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from BEvent_app import get_db

#DA FINIRE BISOGNA MODIFICARE GRAN PARTE DEI DATI

app = Flask(__name__)
app = get_db()


# Funzione per cancellare l'evento dal profilo dell'utente
def cancella_evento_utente(organizzatore_id, evento_id):
    try:
        utente = mongo.db.utenti.find_one({'_id': ObjectId(organizzatore_id)})

        if utente:
            utente['eventi_cancellati'].append(evento_id)
            mongo.db.utenti.update_one({'_id': ObjectId(organizzatore_id)}, {'$set': {'eventi_cancellati': utente['eventi_cancellati']}})
    except Exception as e:
        print(str(e))
        raise

#rendere nuovamente prenotabili le date dei fornitori nel database
def rendi_prenotabili_date_fornitori(fornitori_coinvolti):
    try:
        for fornitore_id in fornitori_coinvolti:
            fornitore = mongo.db.fornitori.find_one({'_id': ObjectId(fornitore_id)})

            if fornitore:
                fornitore['date_disponibili'].append(data_prenotata)
                mongo.db.fornitori.update_one({'_id': ObjectId(fornitore_id)}, {'$set': {'date_disponibili': fornitore['date_disponibili']}})
    except Exception as e:
        print(str(e))
        raise

#  rimborso
def richiedi_rimborso(organizzatore_id, importo):
    try:

        mongo.db.utenti.update_one({'_id': ObjectId(organizzatore_id)}, {'$set': {'rimborso_richiesto': True}})
    except Exception as e:
        print(str(e))
        raise


def avvisa_fornitori(fornitori_coinvolti, titolo_evento):
    try:
        for fornitore_id in fornitori_coinvolti:
            fornitore = mongo.db.fornitori.find_one({'_id': ObjectId(fornitore_id)})

            if fornitore and 'email' in fornitore:
                destinatario_email = fornitore['email']


                soggetto = f"L'evento {titolo_evento} è stato cancellato"
                corpo_email = f"Ciao {fornitore['nome']},\nL'evento {titolo_evento} è stato cancellato. Controlla il tuo profilo per ulteriori dettagli."

                invia_email(destinatario_email, soggetto, corpo_email)
    except Exception as e:
        print(str(e))
        raise


def cancella_evento_db(evento_id):
    try:
        mongo.db.eventi.delete_one({'_id': ObjectId(evento_id)})
    except Exception as e:
        print(str(e))
        raise


def invia_email(destinatario, soggetto, corpo):
    try:

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Autenticazione  account email
        server.login('tuo_email@gmail.com', 'tua_password')


        msg = MIMEMultipart()
        msg['From'] = 'tuo_email@gmail.com'
        msg['To'] = destinatario
        msg['Subject'] = soggetto
        msg.attach(MIMEText(corpo, 'plain'))

        # Invio dell'email
        server.sendmail('tuo_email@gmail.com', destinatario, msg.as_string())

        server.quit()
    except Exception as e:
        print(str(e))
        raise

# cancellazione di un evento
@app.route('/api/eventi/<string:evento_id>', methods=['DELETE'])
def cancella_evento(evento_id):
    try:
        evento = mongo.db.eventi.find_one({'_id': ObjectId(evento_id)})

        if not evento:
            return jsonify({'success': False, 'message': 'Evento non trovato.'}), 404

        organizzatore_id = evento['organizzatore_id']
        fornitori_coinvolti = evento['fornitori']


        cancella_evento_utente(organizzatore_id, evento_id)


        cancella_evento_db(evento_id)


        avvisa_fornitori(fornitori_coinvolti, evento['titolo'])


        rendi_prenotabili_date_fornitori(fornitori_coinvolti)


        richiedi_rimborso(organizzatore_id, evento['costo'])

        return jsonify({'success': True, 'message': 'Evento cancellato con successo.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
