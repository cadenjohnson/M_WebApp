# Script to handle different routes associated with Admin Account
#
# Caden Johnson - 10/30/22

from app import db
from M_models import User

from flask import render_template, redirect, Blueprint
from flask_login import login_required, logout_user, current_user


admin = Blueprint('admin', __name__, template_folder = 'templates')

# route for admin portal (temporary)
@admin.route('/', methods=['GET'])
@login_required
def index():
    return render_template('admin.html')

# route for logging out
@admin.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')


# route for screensaver
@admin.route('/screensaver', methods=['GET'])
@login_required
def screensaver():
    return render_template('screensaver.html')


# route for portfolio site
@admin.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


