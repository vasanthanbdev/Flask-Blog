from flask import request, render_template, Blueprint
from posts.models import Post
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    posts = Post.query.order_by(Post.date_posted.desc())    
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')