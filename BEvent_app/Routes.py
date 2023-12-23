from flask import render_template, Blueprint, session
from flask_login import login_required, current_user



views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('Home.html')


@views.route('/login_page')
def login_page():
    if not current_user.is_authenticated:
        return render_template('Login.html')
    return home()

@views.route('/registrazione_page')
def registrazione_page():
    if not current_user.is_authenticated:
        return render_template('Registrazione.html')
    return home()
