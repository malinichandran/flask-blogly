"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)



@app.route("/users")
def list_users():
    """List Users and show add user button"""

    users = User.query.all()
    return render_template("userlist.html", users=users)

@app.route("/users/new")
def new_user_form():
    """Shows the new user form"""
    return render_template("newuser_form.html")

@app.route("/users/new", methods=["POST"])
def add_new_user():
    """Add new user to the list"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    
    user= User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info about a user"""

    user = User.query.get_or_404(user_id)
    
    posts= Post.query.filter(Post.user_id==user_id)
    return render_template("userdetails.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Show the edit screen for the user"""
    user = User.query.get_or_404(user_id)
    return render_template("editpage.html",user=user)

@app.route("/users/<int:user_id>/edit",methods=["POST"])
def get_edit_data(user_id):
    """Get data from the edit form for the Post request"""
    
    user= User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>/delete",methods=["POST"])
def delete_user(user_id):
    """Deleting a user"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Show the new post form to the user"""
    user = User.query.get_or_404(user_id)
    return render_template("newpostform.html",user=user)

@app.route("/users/<int:user_id>/posts/new",methods=["POST"])
def add_new_post(user_id):
    """Handle the new post form data and add post"""
    user = User.query.get(user_id)
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title,content=content,user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/posts")
def show_all_posts():
    """Shows all posts"""
    posts = Post.query.all()
    return render_template("allposts.html",posts=posts)

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show post details"""
    post = Post.query.get(post_id)
    id = post.user_id
    user = User.query.get(id)
    return render_template("postdetails.html",post=post,user=user)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Show post edit form"""
    post = Post.query.get(post_id)
    id = post.user_id
    user = User.query.get(id)
    return render_template("editpostform.html",post=post,user=user)

@app.route("/posts/<int:post_id>/edit",methods=["POST"])
def handle_edit_postform(post_id):
    """Handle data from the edit post form"""
    post = Post.query.get(post_id)
    id = post.user_id
    user = User.query.get(id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user.id}")

@app.route("/posts/<int:post_id>/delete",methods=["POST"])
def delete_post(post_id):
    """Delete a Post"""
    
    post = Post.query.get(post_id)
    
    Post.query.filter_by(id=post_id).delete()
    id = post.user_id
    user = User.query.get(id)
    db.session.commit()
    return redirect(f"/users/{user.id}")