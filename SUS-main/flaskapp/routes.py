from flask import redirect, url_for, render_template, flash, request, abort
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, TaskForm, UpdateTaskForm, PostForm
from flaskapp.models import User, Task, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import secrets
import os
from datetime import datetime


@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    my_tasks = Task.query.filter_by(user_id=current_user.id).all()
    image_file = url_for('static', filename='images/' +
                         current_user.image_file)
    return render_template('dashboard.html', image_file=image_file, my_tasks=my_tasks, active_page='dashboard')



@app.route("/convo")
def convo():
    posts = Post.query.all()
    return render_template('convo.html', posts=posts)



@app.route("/tasks", methods=['GET', 'POST'])
@login_required
def tasks():
    image_file = url_for('static', filename='images/' +
                         current_user.image_file)
    my_tasks = Task.query.filter_by(user_id=current_user.id).all()
    form = TaskForm()

    if form.validate_on_submit():
        task = Task(title=form.title.data, priority=form.priority.data,
                    date_due=form.date_due.data, todo=form.content.data, creator=current_user)
        db.session.add(task)
        db.session.commit()
        flash('You task has been created!', 'success')
        return redirect(url_for('tasks'))

    return render_template('tasks.html', my_tasks=my_tasks, form=form, image_file=image_file, active_page='tasks')


@app.route("/tasks/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.creator != current_user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.todo = form.content.data
        task.date_due = form.date_due.data
        task.priority = form.priority.data
        db.session.commit()
        flash('Your Task has been updated!', 'success')
        return redirect(url_for('tasks'))
    elif request.method == 'GET':
        form.title.data = task.title
        form.content.data = task.todo
        string_format = task.date_due
        form.date_due.data = datetime.strptime(string_format, '%Y-%m-%d').date()
        form.priority.data = task.priority
        
    return render_template('update.html', form=form, task=task)


@app.route("/tasks/<int:task_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.creator != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('tasks'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' +
                         current_user.image_file)
    return render_template('profile.html', image_file=image_file, form=form, active_page='profile')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has now been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return (redirect(next_page) if next_page else redirect(url_for('dashboard')))
        else:
            flash('Login unsucessful. Please check email and password', 'danger')
    return render_template('properlogin.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/support", methods=['GET', 'POST'])
@login_required
def support():
    image_file = url_for('static', filename='images/' +
                         current_user.image_file)
    return render_template('support.html', active_page='support', image_file=image_file)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post =Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('convo'))
    return render_template('create_post.html', title='New Post', form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('convo'))

@app.route('/ecotips')
def eco_tips():
    # Here you'll add logic to fetch sustainable tips from your API
    # For now, let's just render the template
    return render_template('ecotips.html')