# Script to handle different routes associated with logging in
#
# Caden Johnson - 5/22/22

from app import app
from app import db
from M_models import User

from flask import render_template, request, redirect
from flask_login import login_required, login_user, logout_user, current_user

from flask import Blueprint
from flask import render_template

from flask_login import LoginManager


account = Blueprint('account', __name__, template_folder = 'templates')


# Initiate login manager
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@account.route('/', methods=['GET'])
@login_required
def index():
    return render_template('account.html', account=current_user)


@account.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html', account=current_user)


@account.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        user = User.query.filter_by(username = uname).first()
        if not user or pword != user.password:
            error = 'Nice Try... Invalid'
        else:
            login_user(user)
            return redirect('/account/dashboard')
    return render_template('login.html', error=error)



@account.route('/signup', methods=['GET', 'POST'])
def signup():
    error=None
    if request.method == 'POST':
        email = request.form['email_address']
        uname = request.form['username']
        pword = request.form['password']
        name = request.form['name']

        if User.query.filter_by(email_address = email).first():
            error = 'Account already exists. Please use the login page to gain access.'
        elif User.query.filter_by(username = uname).first():
            error = 'Username is already taken. Please try another.'
        else:
            # Create new user and commit changes to DB
            new_user = User(username=uname, password=pword, email_address=email, name=name)
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect('/account/dashboard')
            except:
                error = 'There was an issue setting up your account. Please contact the Admin.'
    return render_template('signup.html', error=error)



@account.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')



@account.route('/delete/<int:id>')
@login_required
def delete(id):
    account_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(account_to_delete)
        db.session.commit()
        return redirect('/account/login')

    except:
        return render_template('account.html', error='There was a problem deleting your account')
