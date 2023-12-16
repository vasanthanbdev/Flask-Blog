from flask import request, render_template, url_for, flash, redirect, Blueprint
from flaskblog import *
from forms import *
from flaskblog.models import *
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)


#routes for posts
@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/new", method=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been successfully created!', 'sucess')
        return redirect(url_for('home'))
    return render_template('new_post.html', title="New Post", form=form)


@app.route("/post/<int:post_id>/edit", method=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been successfully edited!', 'sucess')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_post.html', title="Edit Post", form=form)


@app.route("/post/<int: post_id>/delete", method=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been successfully deleted!', 'sucess')
    return redirect(url_for('home'))