from flask import Blueprint
from flask import render_template

posts = Blueprint('posts', __name__, template_folder = 'templates')
templets_folder = ('templates')

# localhost:5000/blog/
@posts.route('/')
def posts_list():
    return render_template('posts/posts.html')
    