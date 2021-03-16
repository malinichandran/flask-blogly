"""Blogly application."""

from flask import Flask, request, redirect, render_template,flash
from models import db, connect_db, User, Post, PostTag, Tag

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

@app.route("/")
def show_all_posts():
    """Shows all posts"""
    
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("allposts.html",posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

@app.route("/users")
def list_users():
    """List Users and show add user button"""

    users = User.query.order_by(User.first_name,User.last_name).all()
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
    image_url = request.form['image_url'] or None
    
    user= User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} added.")
    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info about a user"""

    user = User.query.get_or_404(user_id)
    
    return render_template("userdetails.html", user=user)

@app.route("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Show the edit screen for the user"""
    user = User.query.get_or_404(user_id)

    return render_template("edituserpage.html",user=user)


@app.route("/users/<int:user_id>/edit",methods=["POST"])
def get_edit_data(user_id):
    """Get data from the edit form for the Post request"""
    
    user= User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>/delete",methods=["POST"])
def delete_user(user_id):
    """Deleting a user"""
    user = User.query.get(user_id)
    db.session.delete(user)
    
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Show the new post form to the user"""
    user = User.query.get_or_404(user_id)
    tags =  Tag.query.all()
    return render_template("newpostform.html",user=user,tags=tags)

@app.route("/users/<int:user_id>/posts/new",methods=["POST"])
def add_new_post(user_id):
    """Handle the new post form data and add post"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title,content=content,user=user,tags=tags)
    db.session.add(post)
    db.session.commit()
    flash(f"Post {post.title} added")

    return redirect(f"/users/{user.id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show post details"""
    post = Post.query.get_or_404(post_id)
   
    return render_template("postdetails.html",post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Show post edit form"""
    post = Post.query.get_or_404(post_id)
    tags= Tag.query.all()

    return render_template("editpostform.html",post=post,tags=tags)

@app.route("/posts/<int:post_id>/edit",methods=["POST"])
def handle_edit_postform(post_id):
    """Handle data from the edit post form"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    db.session.add(post)
    db.session.commit()
    flash(f"Post {post.title} edited")

    return redirect(f"/users/{post.user.id}")

@app.route("/posts/<int:post_id>/delete",methods=["POST"])
def delete_post(post_id):
    """Delete a Post"""
    
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post {post.title} deleted")

    return redirect(f"/users/{post.user_id}")

@app.route("/tags")
def list_tags():
    """Show all tags"""
    tags = Tag.query.all()

    return render_template("tags.html",tags=tags)

@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """Show tag details"""

    tag = Tag.query.get_or_404(tag_id)
   
    return render_template("tagdetails.html",tag=tag)

@app.route("/tags/new")
def new_tagform():
    """Show form to add new tag"""
    posts= Post.query.all()
    return render_template("newtagform.html",posts=posts)

@app.route("/tags/new",methods=["POST"])
def handle_newtagform():
    """Add new tag"""
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = request.form['name']
    tag = Tag(name=new_tag,posts=posts)
    db.session.add(tag)
    db.session.commit()
    flash(f"New Tag {tag.name} added")

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tagform(tag_id):
    """Show edit tag form"""
    
    tag = Tag.query.get_or_404(tag_id)
    posts= Post.query.all()
    return render_template("edittagform.html",tag=tag,posts=posts)


@app.route("/tags/<int:tag_id>/edit",methods=["POST"])
def handle_edittagform(tag_id):
    """Edit tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    db.session.add(tag)
    db.session.commit()
    flash(f"Tag name edited successfully")
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete",methods=["POST"])
def delete_tag(tag_id):
    """Delete tag"""

    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag name {tag.name} deleted")

    return redirect("/tags")
