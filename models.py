"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):

    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = "https://i.stack.imgur.com/l60Hf.png"

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.Text,
                            nullable=False,
                            unique=True)

    last_name = db.Column(db.Text,
                            nullable=False)

    image_url = db.Column(db.Text,default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.Text,
                      nullable=False)
                

    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime(),
                    default=datetime.datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    @property
    def readable_date(self):
        """Return a user friendly date format"""        
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")   



class PostTag(db.Model):

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True )

class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(50))


    posts = db.relationship('Post',secondary="posttags",
                            backref="tags")                           