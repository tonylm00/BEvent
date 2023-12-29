from flask import render_template, Blueprint, session
from flask_login import current_user

# from flask_login import login_required, current_user
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/fornitore_page')
def fornitore_page():
    return render_template('AreaFornitore.html')


@views.route('/organizzatore_page')
def organizzatore_page():
    return render_template('HomeOrganizzatore.html')


@views.route('/admin_page')
def admin_page():
    return render_template('AreaAdmin.html')

@views.route('/error_page')
def error_page():
    return render_template('ErrorPage.html')

@views.route('/error_page')
def error_page():
    return render_template('ErrorPage.html')


@views.route('/home')
def home():
    return render_template('Home.html')


@views.route('/login_page')
def login_page():
    return render_template('Login.html')


@views.route('/registrazione_page')
def registrazione_page():
    if not current_user.is_authenticated:
        return render_template('Registrazione.html')
    return home()
