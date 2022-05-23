# Script to handle different routes associated with logging in
#
# Caden Johnson - 5/22/22


from app import app
from M_models import User
from flask import render_template, request, redirect, url_for
from flask_login import login_user


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    if request.method == 'POST':
        user = User.query.filter_by(username = request.form['username'])
        if not user or request.form['password'] != user.password:
            error = 'Invalid Credentials. Please try again or create a new account.'
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=None
    if request.method == 'POST':
        if User.query.filter_by(email_address = request.form['email_address']) == True:
            error = 'Account already exists. Please use the login page to gain access.'
        elif User.query.filter_by(username = request.form['username']) == True:
            error = 'Username is already taken. Please try another.'
        else:

            # Create new user and commit changes to DB***********************************************

            return redirect(url_for('home'))
    return render_template('login.html', error=error)
