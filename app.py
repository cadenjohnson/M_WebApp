# Cha boi hit puberty. It's time to take this shit public.
# Caden Johnson is ma dadi
# Rising from the ashes on 5/19/2022
#
# McKracken


from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import login_required, login_user, current_user, LoginManager

# Create instance of flask object
app = Flask(__name__)
app.config.from_object(Config)


# Create database object
db = SQLAlchemy(app)


# Initiate migrate object (keeps track of database history)
migrate = Migrate(app, db)


# Import and register the blueprints
from admin.admin_blue import admin
from blog.blog_blue import posts
from user_account.user_blue import account
from todo.todo_blue import tasks

app.register_blueprint(admin, url_prefix = '/admin')
# localhost:5000/admin

app.register_blueprint(posts, url_prefix = '/blog')
# localhost:5000/blog

app.register_blueprint(account, url_prefix = '/account')
# localhost:5000/account

app.register_blueprint(tasks, url_prefix = '/todo')
# localhost:5000/todo


# Initiate login manager
login_manager = LoginManager()
login_manager.init_app(app)
from M_models import User


# route for loading a user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# index route
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# route for login page
@app.route('/login', methods=['GET', 'POST'])
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
            if uname=='admin' and pword==user.password:
                return redirect('/admin')
            return redirect('/dashboard')
    return render_template('login.html', error=error)


# route for sign up / register page
@app.route('/signup', methods=['GET', 'POST'])
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
                return redirect('/dashboard')
            except:
                error = 'There was an issue setting up your account. Please contact the Admin.'
    return render_template('signup.html', error=error)


# route for account dashboard
@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html', account=current_user)


# error message routes
@app.route('/errorpage', methods=['GET'])
def errorpage():
    return render_template('errorpage.html')


# HTTP error handlers
@app.errorhandler(404)
def send_errorpage(error):
    return render_template('errorpage.html'),404

@app.errorhandler(405)
def send_errorpage(error):
    return render_template('errorpage.html'),405

@app.errorhandler(500)
def send_errorpage(error):
    return render_template('errorpage.html'),500

