"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):

    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                            nullable=False,
                            unique=True)

    last_name = db.Column(db.String(50),
                            nullable=False)

    image_url = db.Column(db.String(100))

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                      nullable=False)
                

    content = db.Column(db.String(1000))

    created_at = db.Column(db.DateTime(),
                    default=datetime.datetime.now)
                            

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    user = db.relationship('User')