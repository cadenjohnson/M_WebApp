# Script to handle different routes associated with logging in
#
# Caden Johnson - 5/22/22

from app import db
from M_models import User

from flask import render_template, redirect, Blueprint
from flask_login import login_required, logout_user, current_user


account = Blueprint('account', __name__, template_folder = 'templates')


# route for account details
@account.route('/', methods=['GET'])
@login_required
def index():
    return render_template('account.html', account=current_user)


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
        return redirect('/account/login')

    except:
        return render_template('account.html', error='There was a problem deleting your account')

