

from flask import Blueprint, redirect, request, render_template
from app import db, current_user
from M_models import Todo
from flask_login import login_required


tasks = Blueprint('tasks', __name__, template_folder = 'templates')


@tasks.route('/', methods=['POST','GET'])
@login_required
def index():
    # for POST requests
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content, user_id=current_user.id)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue adding your task'

    # for GET requests
    else:
        # gets all db contents sorted by date created
        tasks = Todo.query.order_by(Todo.date_created).filter(Todo.user_id==current_user.id).all()

        # searches in the "templates" folder, and grabs specified file
        return render_template('tasks.html', tasks=tasks, user=current_user)


@tasks.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo')

    except:
        return 'There was a problem deleting that task'


@tasks.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/todo')
        
        except:
            return 'There was a problem updating that task'
    else:
        return render_template('update.html', task = task_to_update)