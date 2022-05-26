# Cha boi hit puberty. It's time to take this shit public.
# Caden Johnson is ma dadi
# Rising from the ashes on 5/19/2022
#
# McKracken


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from config import Config


# Create instance of flask object
app = Flask(__name__)
app.config.from_object(Config)


# Create database object
db = SQLAlchemy(app)


# Initiate migrate object (keeps track of database history)
migrate = Migrate(app, db)


# Import and register the blueprints
from blog.blog_blue import posts
from user_account.user_blue import account
from todo.todo_blue import tasks


app.register_blueprint(posts, url_prefix = '/blog')
# localhost:5000/blog

app.register_blueprint(account, url_prefix = '/account')
# localhost:5000/account

app.register_blueprint(tasks, url_prefix = '/todo')
# localhost:5000/todo


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# sets location of database (3 slashes is relative path (4=absolute))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///M_Memory.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
#app.config['SQLALCHEMY_BINDS'] = {'Todo' : 'sqlite:///todo.db',
#                                  'Calendar' : 'sqlite:///calendar.db',
#                                  'Spotify' : 'sqlite:///spotify.db',
#                                  'Weather' : 'sqlite:///weather.db',
#                                  'Cameras' : 'sqlite:///cameras.db',
#                                  'Blog' : 'sqlite:///blog.db'}




