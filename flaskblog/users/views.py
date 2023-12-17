from flask import request, render_template, url_for, flash, redirect, Blueprint
from flaskblog import db
from forms import RegistrationForm, LoginForm
from models import User
from posts.models import Post
from flask_login import login_user, logout_user, login_required, current_user

users = Blueprint('users', __name__)


# routes for user management
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your acccount has been created you can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account/<str:username>")
@login_required
def account(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())
    return render_template('account.html', title='Acccount', user=user, posts=posts)


@users.route("/account/<str:username>/update")
@login_required
def update_account(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = RegistrationForm()
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data
        return redirect(url_for('users.account', username=user.username))
    elif request.method == 'GET':
        form.email.data = user.email
        form.username.data = user.username
        form.password.data = user.password
    return render_template('update_account.html', title="Update Account",form=form)