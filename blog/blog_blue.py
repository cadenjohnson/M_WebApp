from flask import Blueprint
from flask import render_template

from M_models import Blog

posts = Blueprint('posts', __name__, template_folder = 'templates')


# localhost:5000/blog/
@posts.route('/')
def posts_list():
    posts = Blog.query.all()
    return render_template('posts.html', posts=posts)


@posts.route('/<slug>')
def post_detail(slug):
    post = Blog.query.filter(Blog.slug==slug).first()
    return render_template('post_detail.html', post=post)
    