# Cha boi hit puberty. It's time to take this shit public.
# Caden Johnson is ma dadi
# Rising from the ashes on 5/19/2022
#
# McKracken


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from flask_login import LoginManager

from config import Config
from blog.blueprint import posts

# Create instance of flask object
app = Flask(__name__)
app.config.from_object(Config)

# Create database object
db = SQLAlchemy(app)

# Initiate migrate object (keeps track of database history)
migrate = Migrate(app, db)


import M_models

# Initiate login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return M_models.User.query.get(int(user_id))


app.register_blueprint(posts, url_prefix = '/blog')
# localhost:5000/blog




# sets location of database (3 slashes is relative path (4=absolute))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///M_Memory.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
#app.config['SQLALCHEMY_BINDS'] = {'Todo' : 'sqlite:///todo.db',
#                                  'Calendar' : 'sqlite:///calendar.db',
#                                  'Spotify' : 'sqlite:///spotify.db',
#                                  'Weather' : 'sqlite:///weather.db',
#                                  'Cameras' : 'sqlite:///cameras.db',
#                                  'Blog' : 'sqlite:///blog.db'}




