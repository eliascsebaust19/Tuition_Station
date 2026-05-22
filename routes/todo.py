from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, ToDo

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/')
@login_required
def index():
    todos = ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.created_at.desc()).all()
    return render_template('todo/index.html', todos=todos)


@todo_bp.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title', '').strip()
    if not title:
        flash('Title is required.', 'error')
        return redirect(url_for('todo.index'))
    todo = ToDo(user_id=current_user.id, title=title, description=request.form.get('description', ''))
    db.session.add(todo)
    db.session.commit()
    flash('Task added!', 'success')
    return redirect(url_for('todo.index'))


@todo_bp.route('/<int:todo_id>/toggle')
@login_required
def toggle(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('todo.index'))
    todo.is_completed = not todo.is_completed
    db.session.commit()
    return redirect(url_for('todo.index'))


@todo_bp.route('/<int:todo_id>/delete')
@login_required
def delete(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('todo.index'))
    db.session.delete(todo)
    db.session.commit()
    flash('Task deleted.', 'success')
    return redirect(url_for('todo.index'))
