# Script to handle different routes associated with logging in
#
# Caden Johnson - 5/22/22

from app import db
from M_models import User

from flask import render_template, redirect, Blueprint, request
from flask_login import login_required, login_user, logout_user, current_user


account = Blueprint('account', __name__, template_folder = 'templates')


# route for account details
@account.route('/', methods=['GET'])
@login_required
def index():
    return render_template('account.html', account=current_user)


# route for updating account details
@account.route('/updateaccount', methods=['GET', 'POST'])
@login_required
def updateaccount():
    error=None

    currentboi = User.query.filter_by(id = current_user.id).first()

    if request.method == 'POST':
        email = request.form['email_address']
        uname = request.form['username']
        pword = request.form['password']
        pword1 = request.form['password1']
        name = request.form['name']

        if pword != pword1:
            error = 'Passwords entered are not the same. Try again.'

        # Test for attempt at duplicate emails or usernames
        testemail = User.query.filter_by(email_address = email).first()
        if testemail:
            if testemail.id != current_user.id:
                error = 'Email address already registered. Please choose another'

        testuname = User.query.filter_by(username = uname).first() 
        if testuname:
            if testuname.id != current_user.id:
                error = 'Username is already taken. Please choose another'

        if not error:
            # Update user account details and commit changes to DB
            if email:
                currentboi.email_address = email
            if uname:
                currentboi.username = uname
            if pword:
                currentboi.password = pword
            if name:
                currentboi.name = name

            # commit changes to database
            try:
                db.session.commit()
                error='Changes to account updated!'
                return render_template('dashboard.html', error=error)
            except:
                error = 'There was an issue setting up your account. Please contact the Admin.'

    return render_template('updateaccount.html', account=currentboi, error=error)


# route for logging out
@account.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')


# route for deleting the currently signed in account
@account.route('/delete/<int:id>')
@login_required
def delete(id):
    account_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(account_to_delete)
        db.session.commit()
        return redirect('/login')

    except:
        return render_template('account.html', error='There was a problem deleting your account')

